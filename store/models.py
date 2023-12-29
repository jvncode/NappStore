import uuid
from django.db import models
from rest_framework.exceptions import ValidationError

from .constants import COLOURS, SIZE, SIZING, FABRIC, CATEGORIES_CHOICES


class Category(models.Model):
    name = models.CharField(max_length=50, choices=CATEGORIES_CHOICES, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False, related_name='products')
    main_colour = models.CharField(max_length=50, choices=COLOURS, null=False, blank=False, verbose_name='Main colour')
    second_colour = models.CharField(max_length=50, choices=COLOURS, null=False, blank=False,
                                     verbose_name='Secondary colour')
    logo_colour = models.CharField(max_length=50, choices=COLOURS, null=True, blank=True, verbose_name='Logo colour')
    brand = models.CharField(max_length=200, null=False, blank=False, verbose_name='Brand')
    inclusion_date = models.DateTimeField(null=False, blank=False, auto_now_add=True,
                                          verbose_name='Date first inclusion')
    url_img = models.URLField(max_length=500, null=False, blank=False, verbose_name='URL Image')
    price = models.FloatField(null=False, blank=False, verbose_name='Price')
    initial_stock = models.IntegerField(null=False, blank=False, default=10, editable=False,
                                        verbose_name='Initial Stock')
    current_stock = models.IntegerField(null=False, blank=False, verbose_name='Current Stock')
    description = models.TextField(max_length=500, null=False, blank=False, verbose_name='Description')
    size = models.CharField(max_length=200, choices=SIZE, null=True, blank=True, verbose_name='Size')
    sizing = models.CharField(max_length=200, choices=SIZING, null=True, blank=True, verbose_name='Sizing')
    fabric = models.CharField(max_length=50, choices=FABRIC, null=True, blank=True, verbose_name='Fabric')
    sleeve = models.BooleanField(default=True, null=True, blank=True, verbose_name='Sleeve')

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"

    def __str__(self):
        return f"{self.category} | {self.description} | {self.brand}"

    @property
    def is_available(self):
        return self.current_stock > 0


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    # We overwrite this method to check that there is no active cart
    # in order to create another one.
    def save(self, *args, **kwargs):
        current_cart = Cart.objects.all().first()
        if not current_cart or current_cart.completed or self.id == current_cart.id:
            return super(Cart, self).save(*args, **kwargs)
        raise ValidationError("One cart still in progress")


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cart_item')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.description

    def save(self, *args, **kwargs):
        if self.cart.completed:
            raise ValidationError("This cart is now closed, no more products can be added.")
        current_product = Product.objects.filter(id=self.product.id).first()
        if current_product.is_available:
            if current_product.current_stock < self.quantity:
                raise ValidationError("The requested quantity does not exist,"
                                      f" there are {current_product.current_stock} of this product.")
            current_product.current_stock -= self.quantity
            #super(Product, current_product).save(*args, **kwargs)
            return super(CartItem, self).save(*args, **kwargs)
        else:
            raise ValidationError("Product not available")



class Customer(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True, related_name='customer_cart')
    name = models.CharField(max_length=200, blank=False, null=False)
    surname = models.CharField(max_length=300, blank=False, null=False)
    address = models.CharField(max_length=400, blank=False, null=False)
    email = models.EmailField(max_length=200, blank=False, null=False)
    phone = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f"{self.name} {self.surname}"

    # TODO Implement send_mail
