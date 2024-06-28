import logging
import sys
import time
import traceback

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import F

from ...models import CallLog, Queue, Worker, WorkerException, WorkerStatus

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help='worker name')

    def handle(self, *args, **options):
        worker, created = Worker.objects.get_or_create(name=options['name'])
        defaults = dict(started_at=round(time.time(),6))
        WorkerStatus.objects.update_or_create(defaults,worker=worker)
        has_exception = True
        try:
            self.work(worker)
            has_exception = False
        finally:
            if has_exception:
                WorkerException(
                    worker=worker,
                    exc_class=sys.exc_info()[0],
                    exc_message=sys.exc_info()[1],
                    exc_traceback=traceback.format_exc(),
                    created_at=round(time.time(),5),
                )

    def work(self,worker):
        restart_at = None
        if worker.restart_interval:
            restart_at = time.time()+worker.restart_interval
        while not restart_at or time.time() < restart_at:
            for queue in Queue.objects.all():
                try:
                    call_command(queue.name)
                finally:
                    Queue.objects.filter(id=queue.id).delete()
                    CallLog(
                        worker_id=worker.id,
                        name=queue.name,
                        created_at=round(time.time(),5)
                    ).save()
            WorkerStatus.objects.filter(worker_id=worker.id).update(
                updated_at=round(time.time(),6)
            )
            time.sleep(worker.sleep_interval or 0.1)
