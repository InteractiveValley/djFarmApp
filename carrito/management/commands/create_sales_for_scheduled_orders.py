from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


# Class MUST be named 'Command'
class Command(BaseCommand):
    # Displayed from 'manage.py help mycommand'
    help = "Create sales for Scheduled Orders to users"

    # make_option requires options in optparse format
    option_list = BaseCommand.option_list + (
        make_option('--scheduled_order', action='store',
                    dest='scheduled_order',
                    default='',
                    help='create sale for scheduled order ID'),
    )

    def handle(self, *app_labels, **options):
        """
        app_labels - app labels (eg. myapp in "manage.py reset myapp")
        options - configurable command line options
        """
        from datetime import datetime, timedelta
        from usuarios.models import ScheduledOrder
        from carrito.models import Sale, DetailSale, INCOMPLETE, COMPLETE

        now = timezone.localtime(timezone.now())
        scheduled_orders = ScheduledOrder.objects.filter(date_next__lte=now.date())

        scheduled_order_cont = 0
        for scheduled_order in scheduled_orders:
            user = scheduled_order.user
            direction = scheduled_order.direction
            card_conekta = scheduled_order.card_conekta
            product = scheduled_order.product
            quantity = scheduled_order.quantity
            sale = Sale.objects.filter(user=user, direction=direction, scheduled_order=True, status=INCOMPLETE,
                                       card_conekta=card_conekta).first()
            if sale is None:
                sale = Sale.objects.create(user=user, direction=direction, scheduled_order=True, status=INCOMPLETE,
                                           card_conekta=card_conekta, notes="pedido programado")
            detail_sale = DetailSale.objects.create(sale=sale, product=product, quantity=quantity, price=product.price)
            scheduled_order.times = 1
            scheduled_order.save()
            scheduled_order_cont += 1

        sales = Sale.objects.filter(status=INCOMPLETE, scheduled_order=True)

        sale_cont = 0
        for sale in sales:
            sale.status = COMPLETE
            sale.save()
            sale_cont += 1

        fecha1 = timezone.now() + timezone.timedelta(days=1)
        fecha2 = datetime.now() + timedelta(days=1)
        fecha3 = now + timezone.timedelta(days=1)

        return "%s %s %s Schedules: %s. Sales process: %s." % (str(fecha1), str(fecha2), str(fecha3), str(scheduled_order_cont), str(sale_cont))
