### Installation
```bash
$ pip install django-command-cron
```

#### `settings.py`
```python
INSTALLED_APPS+=['django_command_cron']

# command_cron_worker.py settings
COMMAND_CRON_WORKER_SLEEP_INTERVAL=0.1
COMMAND_CRON_WORKER_RESTART_INTERVAL=3600
```
#### `migrate`
```bash
$ python manage.py migrate
```

### Features
+   admin interface

### Management commands
name|description
-|-|-
`command_cron`|call pending commands once
`command_cron_worker`|worker

### Examples
```bash
$ python manage.py command_cron # single run
$ python manage.py command_cron_worker # worker (endless loop)
```

worker
```bash
$ python manage.py command_cron_worker
```

