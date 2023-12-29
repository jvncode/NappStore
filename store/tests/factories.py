import datetime
import factory
from factory.django import DjangoModelFactory

from ..models import Category, Product, Cart, CartItem, Customer
from ..constants import CAPS, WHITE, BLACK, BLUE, SIZE_S, COTTOM, SIZING_MALE


class CategoryFactory(DjangoModelFactory):
    name = CAPS
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
    main_colour = WHITE
    second_colour = BLACK
    logo_colour = BLUE
    size = SIZE_S
    brand = "Brand test"
    fabric = COTTOM
    sizing = SIZING_MALE
    sleeve = True
    inclusion_date = datetime.datetime.now()
    url_img = "www.img_test.com"
    price = 0
    initial_stock = 8
    current_stock = 8
    description = "Product test"

    class Meta:
        model = Product


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart


class CartItemFactory(DjangoModelFactory):
    cart = factory.SubFactory(CartFactory)

    class Meta:
        model = CartItem


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer
