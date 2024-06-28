import time

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

RESTART_AT = time.time() + 3600*24*365*100
RESTART_INTERVAL = getattr(settings,'COMMAND_CRON_WORKER_RESTART_INTERVAL',None)
SLEEP_INTERVAL = getattr(settings,'COMMAND_CRON_WORKER_SLEEP_INTERVAL',0.1)
if RESTART_INTERVAL:
    RESTART_AT = time.time() + RESTART_INTERVAL

class Command(BaseCommand):
    def handle(self, *args, **options):
        while time.time() < RESTART_AT:
            call_command('command_cron')
            time.sleep(SLEEP_INTERVAL)
