"""
Django management command to update order totals.
Useful for recalculating order totals after changes to pricing or delivery costs.
Can be run using: python manage.py update_order_totals
"""

from django.core.management.base import BaseCommand
from checkout.models import Order


class Command(BaseCommand):
    """
    Command to update totals for all orders in the system.
    Recalculates order_total, delivery_cost, and grand_total for each order.
    """
    help = 'Updates all order totals'

    def handle(self, *args, **kwargs):
        """
        Execute the command to update all order totals.
        
        Iterates through all orders and calls update_total() on each one.
        Prints success message with count of updated orders.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
            
        Returns:
            None
        """
        orders = Order.objects.all()
        count = 0
        for order in orders:
            order.update_total()
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} orders'))
