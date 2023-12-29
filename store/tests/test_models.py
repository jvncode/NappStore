import datetime
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from .factories import CategoryFactory, ProductFactory, CartFactory, CustomerFactory, CartItemFactory
from ..constants import WHITE, BLACK, RED, SIZE_XS, COTTOM, SIZING_MALE, CAPS, TSHIRTS
from ..models import CartItem


class CategoryTest(TestCase):
    def test_create_full_data(self):
        category = CategoryFactory(
            name=TSHIRTS,
            created=datetime.datetime.now()
        )
        self.assertEqual(category.name, "tshirts")

    def test_create_empty_data(self):
        category = CategoryFactory()
        self.assertEqual(category.name, "caps")


class ProductTest(TestCase):
    def test_create_full_data(self):
        with self.subTest("New Cap"):
            cap = ProductFactory(
                category=CategoryFactory(name="Cap"),
                main_colour=WHITE,
                second_colour=BLACK,
                logo_colour=RED,
                brand="Nike",
                inclusion_date=datetime.datetime(2020, 10, 20),
                url_img="www.pic_test.com",
                price=18.80,
                initial_stock=4,
                current_stock=8,
                description="Product test"
            )

            self.assertEqual(cap.category.name, "Cap")
            self.assertEqual(cap.main_colour, ('white'))
            self.assertEqual(cap.second_colour, ('black'))
            self.assertEqual(cap.logo_colour, ('red'))
            self.assertEqual(cap.brand, "Nike")
            self.assertEqual(cap.url_img, "www.pic_test.com")
            self.assertEqual(cap.price, 18.80)
            self.assertEqual(cap.initial_stock, 4)
            self.assertEqual(cap.current_stock, 8)
            self.assertEqual(cap.description, "Product test")

        with self.subTest("New T-Shirt"):
            tshirt = ProductFactory(
                category=CategoryFactory(name="T-Shirt"),
                main_colour=WHITE,
                second_colour=BLACK,
                size=SIZE_XS,
                brand="Nike",
                fabric=COTTOM,
                sizing=SIZING_MALE,
                sleeve=True,
                inclusion_date=datetime.datetime(2020, 5, 18),
                url_img="www.pic_test.com",
                price=18.80,
                initial_stock=4,
                current_stock=8,
                description="Product test"
            )

            self.assertEqual(tshirt.category.name, "T-Shirt")
            self.assertEqual(tshirt.main_colour, ('white'))
            self.assertEqual(tshirt.second_colour, ('black'))
            self.assertEqual(tshirt.size, ('extra_small'))
            self.assertEqual(tshirt.brand, "Nike")
            self.assertEqual(tshirt.fabric, "cottom")
            self.assertEqual(tshirt.sizing, "male")
            self.assertEqual(tshirt.sleeve, True)
            self.assertEqual(tshirt.url_img, "www.pic_test.com")
            self.assertEqual(tshirt.price, 18.80)
            self.assertEqual(tshirt.initial_stock, 4)
            self.assertEqual(tshirt.current_stock, 8)
            self.assertEqual(tshirt.description, "Product test")

    def test_create_empty_data(self):
        with self.subTest("New Cap"):
            cap = ProductFactory(
                category=CategoryFactory(name="Cap")
            )
            self.assertEqual(cap.category.name, "Cap")
            self.assertEqual(cap.main_colour, ("white"))
            self.assertEqual(cap.second_colour, ("black"))
            self.assertEqual(cap.logo_colour, ("blue"))
            self.assertEqual(cap.brand, "Brand test")
            self.assertEqual(cap.url_img, "www.img_test.com")
            self.assertEqual(cap.price, 0)
            self.assertEqual(cap.initial_stock, 8)
            self.assertEqual(cap.current_stock, 8)
            self.assertEqual(cap.description, "Product test")

        with self.subTest("New T-Shirt"):
            tshirt = ProductFactory(
                category=CategoryFactory(name="T-Shirt")
            )
            self.assertEqual(tshirt.category.name, "T-Shirt")
            self.assertEqual(tshirt.main_colour, ("white"))
            self.assertEqual(tshirt.second_colour, ("black"))
            self.assertEqual(tshirt.size, ("small"))
            self.assertEqual(tshirt.brand, "Brand test")
            self.assertEqual(tshirt.fabric, "cottom")
            self.assertEqual(tshirt.sizing, "male")
            self.assertEqual(tshirt.sleeve, True)
            self.assertEqual(tshirt.url_img, "www.img_test.com")
            self.assertEqual(tshirt.price, 0)
            self.assertEqual(tshirt.initial_stock, 8)
            self.assertEqual(tshirt.current_stock, 8)
            self.assertEqual(tshirt.description, "Product test")

    def test_is_available(self):
        with self.subTest("In stock"):
            tshirt = ProductFactory(
                category=CategoryFactory(name="T-Shirt"),
                current_stock=20,
            )

            stock = tshirt.is_available
            self.assertTrue(stock)

        with self.subTest("Out of Stock"):
            tshirt = ProductFactory(
                category=CategoryFactory(name="T-Shirt"),
                current_stock=0,
            )
            stock = tshirt.is_available
            self.assertFalse(stock)


class CartTest(TestCase):
    def test_no_current_cart_created(self):
        cart = CartFactory(
            id='c167678d-702d-49fc-a84f-492d9bcbad87',
            completed=False,
        )
        self.assertEqual(cart.id, "c167678d-702d-49fc-a84f-492d9bcbad87")
        self.assertFalse(cart.completed)

    def test_current_cart_created_and_completed(self):
        CartFactory(
            id='c167678d-702d-49fc-a84f-492d9bcbad00',
            completed=True,
        )
        cart2 = CartFactory(
            id='c167678d-702d-49fc-a84f-492d9bcbad66',
            completed=False,
        )
        self.assertEqual(cart2.id, "c167678d-702d-49fc-a84f-492d9bcbad66")
        self.assertFalse(cart2.completed)

    def test_current_cart_created_and_not_completed(self):
        CartFactory(
            id='c167678d-702d-49fc-a84f-492d9bcbad98',
            completed=False,
        )
        with self.assertRaises(ValidationError):
            CartFactory(
                id='c167678d-702d-49fc-a84f-492d9bcbad98',
            )


class CartItemTest(TestCase):
    def test_add_product_on_stock(self):
        cart = CartFactory(
            id='c167678d-702d-49fc-a84f-492d9bcbad82',
        )
        cap = ProductFactory(
            category=CategoryFactory(name=CAPS),
        )
        cart_item = CartItemFactory(
            cart=cart,
            product=cap,
            quantity=2,
        )

        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(cart_item.cart.id, 'c167678d-702d-49fc-a84f-492d9bcbad82')
        self.assertEqual(cart_item.product.category.name, "caps")
        self.assertTrue(cart_item.product.is_available)
        self.assertEqual(cart_item.quantity, 2)

    def test_add_product_out_of_stock(self):
        cart = CartFactory(
            id='c167678d-702d-49fc-a84f-492d9bcbad44',
        )
        cap = ProductFactory(
            category=CategoryFactory(name=CAPS),
            current_stock=0,
        )
        with self.assertRaises(ValidationError):
            CartItemFactory(
                cart=cart,
                product=cap,
                quantity=2,
            )


class CustomerTest(TestCase):
    def test_create(self):
        cart = CartFactory(
            id='c167678d-702d-49fc-a84f-492d9bcbad87',
        )
        customer = CustomerFactory(
            cart=cart,
            name="John",
            surname="Smith",
            address="Consell",
            email="jvn@gmail.com",
            phone="+34 658994433",
        )
        self.assertEqual(customer.__str__(), "John Smith")
