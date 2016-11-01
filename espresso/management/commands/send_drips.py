from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        from espresso.models import Drip

        for drip in Drip.objects.filter(enabled=True):
            drip.drip.run()
