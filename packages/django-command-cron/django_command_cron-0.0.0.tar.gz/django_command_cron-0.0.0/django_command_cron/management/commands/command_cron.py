import time

from django.core.management import call_command
from django.core.management.base import BaseCommand

from ...models import CommandCron

class Command(BaseCommand):
    def handle(self, *args, **options):
        for c in CommandCron.objects.all():
            if not c.called_at or c.called_at+c.interval<time.time():
                CommandCron.objects.filter(id=c.id).update(
                    called_at=round(time.time(),5)
                )
                call_command(c.name)
