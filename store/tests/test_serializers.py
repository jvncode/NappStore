from freezegun import freeze_time
from django.test import TestCase
from rest_framework.exceptions import ValidationError

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
                'name': 'Name test',
                'created': output['created'],
                'updated': output['updated'],
            }
        )


class CapSerializerTest(TestCase):
    def test_serializer(self):
        cap = ProductFactory(category=CategoryFactory(name="cap"))

        output = CapSerializer(cap).data
        self.assertDictEqual(
            output,
            {
                'category': 1,
                'main_colour': 'white',
                'second_colour': 'black',
                'logo_colour': 'green',
                'brand': 'Brand test',
                'inclusion_date': output["inclusion_date"],
                'url_img': 'www.img_test.com',
                'price': 0.0,
                'initial_stock': 0,
                'current_stock': 0,
                'description': 'Product test'
            }
        )


class TShirtSerializerTest(TestCase):
    def test_serializer(self):
        tshirt = ProductFactory(category=CategoryFactory(name="tshirt"))

        output = TShirtSerializer(tshirt).data
        self.assertDictEqual(
            output,
            {
                'category': 1,
                'main_colour': 'white',
                'second_colour': 'black',
                'brand': 'Brand test',
                'inclusion_date': output["inclusion_date"],
                'url_img': 'www.img_test.com',
                'price': 0.0,
                'initial_stock': 0,
                'current_stock': 0,
                'description': 'Product test',
                'size': 'small',
                'sizing': 'male',
                'fabric': 'cottom',
                'sleeve': True
            }
        )


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.product = ProductFactory(
            category=CategoryFactory()
        )
        self.cap = ProductFactory(
            category=CategoryFactory(name="cap")
        )
        self.tshirt = ProductFactory(
            category=CategoryFactory(name="tshirt")
        )

    def test_serializer(self):
        output = ProductSerializer(self.product).data
        self.assertDictEqual(
            output,
            {
                'id': output["id"],
                'category': 1,
                'category_name': 'Name test',
                'main_colour': 'white',
                'second_colour': 'black',
                'logo_colour': 'green',
                'brand': 'Brand test',
                'inclusion_date': output["inclusion_date"],
                'url_img': 'www.img_test.com',
                'price': 0.0,
                'current_stock': 0,
                'description': 'Product test',
                'size': 'small',
                'sizing': 'male',
                'fabric': 'cottom',
                'sleeve': True,
            }
        )

    def test_get_caps(self):
        with self.subTest("Cap data object"):
            output_cap = ProductSerializer().get_caps(self.cap).data
            self.assertDictEqual(
                output_cap,
                {
                    'category': 2,
                    'main_colour': 'white',
                    'second_colour': 'black',
                    'logo_colour': 'green',
                    'brand': 'Brand test',
                    'inclusion_date': output_cap["inclusion_date"],
                    'url_img': 'www.img_test.com',
                    'price': 0.0,
                    'initial_stock': 0,
                    'current_stock': 0,
                    'description': 'Product test'
                }
            )
        with self.subTest("Other data object"):
            output_cap = ProductSerializer().get_caps(self.tshirt)
            self.assertIsNone(output_cap)

    def test_get_tshirts(self):
        with self.subTest("T-Shirt data object"):
            output = ProductSerializer().get_tshirts(self.tshirt).data
            self.assertDictEqual(
                output,
                {
                    'category': 3,
                    'main_colour': 'white',
                    'second_colour': 'black',
                    'brand': 'Brand test',
                    'inclusion_date': output["inclusion_date"],
                    'url_img': 'www.img_test.com',
                    'price': 0.0,
                    'initial_stock': 0,
                    'current_stock': 0,
                    'description': 'Product test',
                    'size': 'small',
                    'sizing': 'male',
                    'fabric': 'cottom',
                    'sleeve': True
                }
            )
        with self.subTest("Other data object"):
            output_cap = ProductSerializer().get_tshirts(self.cap)
            self.assertIsNone(output_cap)


class SimpleProductSerializerTest(TestCase):
    def test_serializer(self):
        cap = ProductFactory(
            category=CategoryFactory(name="cap"),
            price=18.20,
        )
        output = SimpleProductSerializer(cap).data
        self.assertDictEqual(
            output,
            {
                'id': 1,
                'category_name': 'cap',
                'description': 'Product test',
                'price': 18.20,
            }
        )


class CartItemsSerializerTest(TestCase):
    def test_serializer(self):
        cart = CartFactory(id="f7b3a040-f486-44e8-a7b5-b23688397bd7")
        cap = ProductFactory(
            category=CategoryFactory(name="cap"),
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
                    'id': 1,
                    'category_name': 'cap',
                    'description': 'Product test',
                    'price': 20.4,
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
            category=CategoryFactory(name="cap"),
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
        self.maxDiff = None
        cart = CartFactory(
            id='c167678d-702d-49fc-a84f-492d9bcbad87',
            created="2023-12-01",
            completed=False,
        )
        cap = ProductFactory(
            category=CategoryFactory(name="cap"),
            price=20.40,
        )
        tshirt = ProductFactory(
            category=CategoryFactory(name="tshirt"),
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
                    'id': 1,
                    'category_name': 'cap',
                    'description': 'Product test',
                    'price': 20.4
                },
        )
        self.assertEqual(output['items'][0]['quantity'], 2),
        self.assertEqual(output['items'][0]['sub_total'], 40.8),
        self.assertEqual(output['total'], 96.3)
        self.assertEqual(output['created'], '2023-12-01T00:00:00')
        self.assertFalse(output['completed'])
