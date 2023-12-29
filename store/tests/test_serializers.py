from freezegun import freeze_time
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from ..constants import CAPS, TSHIRTS
from ..serializers import CategorySerializer, ProductSerializer, CartSerializer, TShirtSerializer, CartItemSerializer, \
    CapSerializer, SimpleProductSerializer, AddCartItemSerializer
from .factories import CategoryFactory, ProductFactory, CartFactory, CartItemFactory


class CategorySerializerTest(TestCase):
    def test_serializer(self):
        category = CategoryFactory()

        output = CategorySerializer(category).data
        self.assertDictEqual(
            output,
            {
                'id': output['id'],
                'name': 'caps',
                'created': output['created'],
                'updated': output['updated'],
            }
        )


class CapSerializerTest(TestCase):
    def test_serializer(self):
        cap = ProductFactory(category=CategoryFactory(name=CAPS))

        output = CapSerializer(cap).data
        self.assertDictEqual(
            output,
            {
                'id': 1,
                'category': 1,
                'category_name': 'caps',
                'main_colour': 'white',
                'second_colour': 'black',
                'logo_colour': 'blue',
                'brand': 'Brand test',
                'inclusion_date': output["inclusion_date"],
                'url_img': 'www.img_test.com',
                'price': 0.0,
                'product_available': True,
                'current_stock': 8,
                'description': 'Product test',
            }
        )


class TShirtSerializerTest(TestCase):
    def test_serializer(self):
        tshirt = ProductFactory(category=CategoryFactory(name=TSHIRTS))

        output = TShirtSerializer(tshirt).data
        self.assertDictEqual(
            output,
            {
                'id': 1,
                'category': 1,
                'category_name': 'tshirts',
                'main_colour': 'white',
                'second_colour': 'black',
                'brand': 'Brand test',
                'inclusion_date': output["inclusion_date"],
                'url_img': 'www.img_test.com',
                'price': 0.0,
                'product_available': True,
                'current_stock': 8,
                'description': 'Product test',
                'size': 'small',
                'sizing': 'male',
                'fabric': 'cottom',
                'sleeve': True,
            }
        )


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.cap = ProductFactory(
            category=CategoryFactory(name=CAPS)
        )

    def test_serializer(self):
        output = ProductSerializer(self.cap).data
        self.assertDictEqual(
            output,
            {
                'id': 1,
                'category': 1,
                'category_name': 'caps',
                'main_colour': 'white',
                'second_colour': 'black',
                'logo_colour': 'blue',
                'brand': 'Brand test',
                'inclusion_date': output["inclusion_date"],
                'url_img': 'www.img_test.com',
                'price': 0.0,
                'product_available': True,
                'current_stock': 8,
                'description': 'Product test',
                'size': 'small',
                'sizing': 'male',
                'fabric': 'cottom',
                'sleeve': True,
            }
        )


class SimpleProductSerializerTest(TestCase):
    def test_serializer(self):
        cap = ProductFactory(
            category=CategoryFactory(name=CAPS),
            price=18.20,
        )
        output = SimpleProductSerializer(cap).data
        self.assertDictEqual(
            output,
            {
                'id': 1,
                'category_name': 'caps',
                'description': 'Product test',
                'price': 18.20,
                'product_available': True,
            }
        )


@freeze_time("2023-12-01 00:00:00")
class CartItemSerializerTest(TestCase):
    def test_serializer(self):
        cart = CartFactory(id="f7b3a040-f486-44e8-a7b5-b23688397bd7")
        cap = ProductFactory(
            category=CategoryFactory(name=CAPS),
            price=20.40,
        )
        trolley = CartItemFactory(
            cart=cart,
            product=cap,
            quantity=2,
        )

        output = CartItemSerializer(trolley).data
        self.assertDictEqual(
            output,
            {
                'id': 1,
                'cart': 'f7b3a040-f486-44e8-a7b5-b23688397bd7',
                'product': {
                    'id': 1,
                    'category_name': 'caps',
                    'description': 'Product test',
                    'price': 20.4,
                    'product_available': True,
                },
                'quantity': 2,
                'sub_total': 40.8,
            }
        )


class AddCartItemSerializerTest(TestCase):
    def setUp(self):
        self.cart = CartFactory(
            id='c167678d-702d-49fc-a84f-492d9bcbad87',
        )
        self.cap = ProductFactory(
            category=CategoryFactory(name=CAPS),
        )
        self.items = CartItemFactory(
            cart=self.cart,
            product=self.cap,
            quantity=2,
        )

    def test_serializer(self):
        output = AddCartItemSerializer(self.items).data
        self.assertDictEqual(
            output,
            {'id': 1, 'product_id': '1', 'quantity': 2}
        )

    def test_validate_product_id(self):
        with self.subTest("Existing product"):
            output = AddCartItemSerializer().validate_product_id(self.cap.id)
            self.assertEqual(output, 1)

        with self.subTest("Non-existing product"):
            with self.assertRaises(ValidationError):
                AddCartItemSerializer().validate_product_id(None)


@freeze_time("2023-12-01 00:00:00")
class CartSerializerTest(TestCase):
    def test_serializer(self):
        cart = CartFactory(
            id='c167678d-702d-49fc-a84f-492d9bcbad87',
            completed=False,
        )
        cap = ProductFactory(
            category=CategoryFactory(name=CAPS),
            price=20.40,
        )
        tshirt = ProductFactory(
            category=CategoryFactory(name=TSHIRTS),
            price=18.50,
        )
        CartItemFactory(
            cart=cart,
            product=cap,
            quantity=2,
        )
        CartItemFactory(
            cart=cart,
            product=tshirt,
            quantity=3,
        )

        output = CartSerializer(cart).data
        self.assertEqual(output['id'], 'c167678d-702d-49fc-a84f-492d9bcbad87')
        self.assertEqual(
            output['items'][0],
            {
                'product__id': 1,
                'product__description': 'Product test',
                'product__price': 20.4
            },
        )
        self.assertEqual(
            output['items'][1],
            {
                'product__id': 2,
                'product__description': 'Product test',
                'product__price': 18.5
            },
        )
        self.assertEqual(output['total'], 38.9)
        self.assertEqual(output['created'], '2023-12-01T00:00:00')
        self.assertFalse(output['completed'])
