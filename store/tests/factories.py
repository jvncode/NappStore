import datetime
import factory
from factory.django import DjangoModelFactory

from ..models import Category, Product, Cart, CartItems, Customer
from ..constants import COLOURS, SIZE, SIZING, FABRIC


class CategoryFactory(DjangoModelFactory):
    name = "Name test"
    created = datetime.datetime(
        day=18,
        month=5,
        year=2020,
        hour=10,
        minute=15,
    )

    class Meta:
        model = Category


class ProductFactory(DjangoModelFactory):
    category = factory.SubFactory(CategoryFactory)
    main_colour = COLOURS[0][0]
    second_colour = COLOURS[1][0]
    logo_colour = COLOURS[3][0]
    size = SIZE[1][0]
    brand = "Brand test"
    fabric = FABRIC[0][0]
    sizing = SIZING[0][0]
    sleeve = True
    inclusion_date = datetime.datetime.now()
    url_img = "www.img_test.com"
    price = 0
    initial_stock = 0
    current_stock = 0
    description = "Product test"

    class Meta:
        model = Product


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart


class CartItemsFactory(DjangoModelFactory):
    cart = factory.SubFactory(CartFactory)

    class Meta:
        model = CartItems


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer
