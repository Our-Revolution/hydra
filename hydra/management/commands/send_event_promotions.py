from django.core.management.bse import BaseCommand, CommandError
from hydra.models import EventPromotionRequest


class Command(BaseCommand):
    help = 'Fulfills sending event promotions marked \'approved\''

    def handle(self, *args, **options):
        EventPromotionRequest._send_approved_emails()