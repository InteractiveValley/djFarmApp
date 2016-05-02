from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


# Class MUST be named 'Command'
class Command(BaseCommand):
    # Displayed from 'manage.py help mycommand'
    help = "Delete all receipt for expiration"

    # make_option requires options in optparse format
    option_list = BaseCommand.option_list + (
        make_option('--receipt_id', action='store',
                    dest='receipt_id',
                    default='',
                    help='ID for Receipt'),
    )

    def handle(self, *app_labels, **options):
        """
        app_labels - app labels (eg. myapp in "manage.py reset myapp")
        options - configurable command line options
        """
        from carrito.models import Receipt, TYPE_OBSOLETE, TYPE_RECEIPT

        now = timezone.localtime(timezone.now())
        receipts = Receipt.objects.filter(date_expiration__lte=now.date(), type_receipt=TYPE_RECEIPT)

        receipts_cont = 0
        for receipt in receipts:
            receipt.type_receipt = TYPE_OBSOLETE
            receipt.status = False
            receipt.save()
            receipts_cont += 1

        return "%s Caducaron: %s. Productos." % (str(now), str(receipts_cont))
