from django.contrib import admin
from .models import Product, Category, Cart, CartItem, Customer


class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'completed')
    search_fields = ('created', 'completed')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart', 'product')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('description', 'brand', 'price', 'current_stock', 'inclusion_date', 'is_available')
    search_fields = ('brand',  'main_colourmain_colour', 'is_available')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Customer)
