from ..products.models import ShoppingCartItem
from django.db import transaction
from django.contrib import messages
from ..utils import get_session
from ..payments.utils.decorators import payment_process
from .models import Order, OrderProduct


def get_total(session):
    items = ShoppingCartItem.objects.filter(cart=session)
    total = sum(item.product.price * item.quantity for item in items)
    return total


@transaction.atomic
@payment_process
def submit_payment(request, session):
    items = ShoppingCartItem.objects.filter(cart=session)
    total = sum(item.product.price * item.quantity for item in items)
    order = Order.objects.create(session=session, amount=total)
    
    if not items:
        messages.error(request, f"You have no products in your cart")
        return False
    
    for item in items:
        try:
            item.product.stock -= item.quantity

            session = get_session(request)

            OrderProduct.objects.create(order=order, item=item, quantity=item.quantity)
            
            item.delete()
            item.product.save()

        except Exception as e:
            messages.error(request, f"Error processing payment: {e}")
            return False

    messages.success(request, "Payment successful! Your order has been placed.")
    return True
