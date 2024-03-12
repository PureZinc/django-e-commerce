from .models import ShoppingCartItem
from django.db import transaction
from django.contrib import messages
from ..utils import get_session


@transaction.atomic
def add_to_cart(request, product, quantity):
    session = get_session(request)
    item, created_item = ShoppingCartItem.objects.get_or_create(product=product, cart=session)
    
    if product.stock < item.quantity + quantity:
        messages.error(request, "Product out of stock!")
        if product.stock == 0:
            item.delete()
        return None
    
    item.quantity += quantity
    item.save()
    
    messages.success(request, f"Successfully added {item.quantity} {item.product.name}'s! You have {item.quantity} {item.product.name}'s in your cart!")


@transaction.atomic
def remove_from_cart(request, product, quantity):
    session = get_session(request)
    item, created_item = ShoppingCartItem.objects.get_or_create(product=product, cart=session)
    
    item.quantity -= quantity
    item.save()
    if item.quantity <= 0:
        item.delete()

    messages.success(request, f"Successfully {item.quantity} {item.product.name}'s! You have {item.quantity} {item.product.name}'s in your cart!")
