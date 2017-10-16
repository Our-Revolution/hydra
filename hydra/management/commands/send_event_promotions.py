from django.core.management.base import BaseCommand, CommandError
from hydra.models import EventPromotionRequest
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fulfills sending event promotions marked \'approved\''

    def handle(self, *args, **options):
        logger.debug('Running send_event_promotions.py')
        EventPromotionRequest._send_approved_emails()
        EventPromotionRequest._mark_approved_as_skipped()
