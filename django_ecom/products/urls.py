from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductsView.as_view(), name='products'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('my-cart/', views.MyCartView.as_view(), name='my_cart'),
    path('add-to-cart/<int:id>/<int:quantity>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove-from-cart/<int:id>/<int:quantity>/', views.add_to_cart_view, name='remove_from_cart'),
]