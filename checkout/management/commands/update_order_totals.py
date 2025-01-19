from django.core.management.base import BaseCommand
from checkout.models import Order

class Command(BaseCommand):
    help = 'Updates all order totals'

    def handle(self, *args, **kwargs):
        orders = Order.objects.all()
        count = 0
        for order in orders:
            order.update_total()
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} orders'))
