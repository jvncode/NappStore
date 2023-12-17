from freezegun import freeze_time
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from ..constants import CAPS, TSHIRTS
from ..serializers import CategorySerializer, ProductSerializer, CartSerializer, TShirtSerializer, CartItemsSerializer, \
    CapSerializer, SimpleProductSerializer, AddCartItemSerializer
from .factories import CategoryFactory, ProductFactory, CartFactory, CartItemsFactory


class CategorySerializerTest(TestCase):
    def test_serializer(self):
        category = CategoryFactory()

        output = CategorySerializer(category).data
        self.assertDictEqual(
            output,
            {
                'id': output['id'],
                'category': 'caps',
                'created': output['created'],
                'updated': output['updated'],
            }
        )


class CapSerializerTest(TestCase):
    def test_serializer(self):
        cap = ProductFactory(category=CategoryFactory(category=CAPS))

        output = CapSerializer(cap).data
        self.assertDictEqual(
            output,
            {
                'id': 2,
                'category': "caps",
                'category_name': 'caps',
                'main_colour': 'white',
                'second_colour': 'black',
                'logo_colour': 'green',
                'brand': 'Brand test',
                'inclusion_date': output["inclusion_date"],
                'url_img': 'www.img_test.com',
                'price': 0.0,
                'product_available': True,
                'current_stock': 8,
                'description': 'Product test',
                'created': output['created'],
                'updated': output['updated'],
            }
        )


class TShirtSerializerTest(TestCase):
    def test_serializer(self):
        tshirt = ProductFactory(category=CategoryFactory(category=TSHIRTS))

        output = TShirtSerializer(tshirt).data
        self.assertDictEqual(
            output,
            {
                'id': 2,
                'category': 'tshirts',
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
                'created': output['created'],
                'updated': output['updated'],
            }
        )


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.cap = ProductFactory(
            category=CategoryFactory(category=CAPS)
        )

    def test_serializer(self):
        output = ProductSerializer(self.cap).data
        self.assertDictEqual(
            output,
            {
                'id': 2,
                'category': "caps",
                'category_name': 'caps',
                'main_colour': 'white',
                'second_colour': 'black',
                'logo_colour': 'green',
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
            category=CategoryFactory(category=CAPS),
            price=18.20,
        )
        output = SimpleProductSerializer(cap).data
        self.assertDictEqual(
            output,
            {
                'id': 2,
                'category_name': 'caps',
                'description': 'Product test',
                'price': 18.20,
                'product_available': True,
                'created': output['created'],
                'updated': output['updated']
            }
        )


@freeze_time("2023-12-01 00:00:00")
class CartItemsSerializerTest(TestCase):
    def test_serializer(self):
        cart = CartFactory(id="f7b3a040-f486-44e8-a7b5-b23688397bd7")
        cap = ProductFactory(
            category=CategoryFactory(category=CAPS),
            price=20.40,
        )
        trolley = CartItemsFactory(
            cart=cart,
            product=cap,
            quantity=2,
        )

        output = CartItemsSerializer(trolley).data
        self.assertDictEqual(
            output,
            {
                'id': 1,
                'cart': 'f7b3a040-f486-44e8-a7b5-b23688397bd7',
                'product': {
                    'id': 2,
                    'category_name': 'caps',
                    'description': 'Product test',
                    'price': 20.4,
                    'product_available': True,
                    'created': "2023-12-01T00:00:00",
                    'updated': "2023-12-01T00:00:00",
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
            category=CategoryFactory(category=CAPS),
        )
        self.items = CartItemsFactory(
            cart=self.cart,
            product=self.cap,
            quantity=2,
        )

    def test_serializer(self):
        output = AddCartItemSerializer(self.items).data
        self.assertDictEqual(
            output,
            {'id': 1, 'product_id': '2', 'quantity': 2}
        )

    def test_validate_product_id(self):
        with self.subTest("Existing product"):
            output = AddCartItemSerializer().validate_product_id(self.cap.id)
            self.assertEqual(output, 2)

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
            category=CategoryFactory(category=CAPS),
            price=20.40,
        )
        tshirt = ProductFactory(
            category=CategoryFactory(category=TSHIRTS),
            price=18.50,
        )
        CartItemsFactory(
            cart=cart,
            product=cap,
            quantity=2,
        )
        CartItemsFactory(
            cart=cart,
            product=tshirt,
            quantity=3,
        )

        output = CartSerializer(cart).data
        self.assertEqual(output['id'], 'c167678d-702d-49fc-a84f-492d9bcbad87')
        self.assertEqual(
            output['items'][0]['product'],
            {
                'id': 2,
                'description': 'Product test',
                'price': 20.4,
                'product_available': True,
                'created': "2023-12-01T00:00:00",
                'updated': "2023-12-01T00:00:00",
            },
        )
        self.assertEqual(output['items'][0]['quantity'], 2),
        self.assertEqual(output['items'][0]['sub_total'], 40.8),
        self.assertEqual(output['total'], 96.3)
        self.assertEqual(output['created'], '2023-12-01T00:00:00')
        self.assertFalse(output['completed'])
