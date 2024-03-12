from django.shortcuts import redirect
from django.views import generic
from .models import Product, ProductImage, ShoppingCartItem
from ..utils import get_session
from .utils import add_to_cart, remove_from_cart

# Create your views here.


class ProductsView(generic.ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/products.html'


class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'products/product_details.html'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        product = self.get_object()
        images = ProductImage.objects.filter(product=product)
        context = super().get_context_data(**kwargs)
        context["images"] = images if images else None
        return context


class MyCartView(generic.ListView):
    model = ShoppingCartItem
    context_object_name = 'items'
    template_name = 'products/my_cart.html'

    def get_queryset(self):
        my_session = get_session(self.request)
        return ShoppingCartItem.objects.filter(cart=my_session)
    
    def get_context_data(self, **kwargs):
        items = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['total_price'] = sum(item.product.price * item.quantity for item in items) if items else 0
        return context
    

# Utility Views
def add_to_cart_view(request, id, quantity):
    product = Product.objects.get(id=id)
    add_to_cart(request, product, quantity)
    return redirect('product_detail', product.slug)

def remove_from_cart_view(request, id, quantity):
    product = Product.objects.get(id=id)
    remove_from_cart(request, product, quantity)
    return redirect('my_cart')
