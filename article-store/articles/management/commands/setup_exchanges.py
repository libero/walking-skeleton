import logging

from django.core.management.base import BaseCommand
from events.utils import declare_exchanges

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Setup default exchanges for target message broker'

    def handle(self, *args, **options):
        declare_exchanges()
