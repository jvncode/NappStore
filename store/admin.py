from django.contrib import admin
from .models import Product, Category, Cart, CartItems, Customer

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItems)
admin.site.register(Customer)

