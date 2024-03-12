from django.contrib import admin
from .orders.models import Order, OrderProduct
from .products.models import Product, ProductImage, ShoppingCartItem


admin.site.register(Order)
admin.site.register(OrderProduct)

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ShoppingCartItem)
