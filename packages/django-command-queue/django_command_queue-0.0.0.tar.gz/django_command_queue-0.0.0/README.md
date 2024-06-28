### Installation
```bash
$ pip install django-command-queue
```

#### `settings.py`
```python
INSTALLED_APPS+=['django_command_queue']
```

#### `migrate`
```bash
$ python manage.py migrate
```

### Features
+   mutiple workers
    +   custom settings
    +   worker status
+   command calls log
+   exceptions logging

### Models
model|db_table|fields/columns
-|-|-
`Queue`|`django`|`id`,`worker`,`name`
`Worker`|`redis_push`|`id`,`worker`,`restart_interval`,`sleep_interval`
`WorkerException`|`redis_push`|`id`,`worker`,`exc_class`,`exc_message`,`exc_traceback`,`created_at`
`WorkerStatus`|`redis_push`|`id`,`worker_id`,`started_at`,`updated_at`

### Management commands
name|description
-|-
`command_queue_worker`|queue worker

### Examples
```bash
$ python manage.py command_queue_worker "name"
```

