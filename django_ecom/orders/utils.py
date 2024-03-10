from .models import ShoppingCartItem
from django.db import transaction
from django.contrib import messages
from django_ecom.utils import get_session
from payments.utils import payment_process
from .models import Order, OrderProduct


@transaction.atomic
@payment_process
def submit_payment(request, total_price, cart):
    items = ShoppingCartItem.objects.filter(cart=cart)
    order = Order.objects.create(session=session, amount=total_price)
    
    if not items:
        messages.error(request, f"You have no products in your cart")
        return None
    
    for item in items:
        try:
            item.product.stock -= item.quantity

            session = get_session(request)

            OrderProduct.objects.create(order=order, item=item, quantity=item.quantity)
            
            item.delete()
            item.product.save()

        except Exception as e:
            messages.error(request, f"Error processing payment: {e}")

    messages.success(request, "Payment successful! Your order has been placed.")
