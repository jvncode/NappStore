from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Sum

from .models import Category, Product, Cart, CartItem, Customer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source="category.name")
    product_available = serializers.SerializerMethodField(method_name="is_available")

    class Meta:
        model = Product
        exclude = ['initial_stock']

    @staticmethod
    def is_available(product: Product):
        return product.is_available


class CapSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        exclude = [
            'initial_stock',
            'size',
            'sizing',
            'fabric',
            'sleeve',
        ]


class TShirtSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        exclude = [
            'logo_colour',
            'initial_stock',

        ]


class SimpleProductSerializer(ProductSerializer):
    category_name = serializers.StringRelatedField(source="category.name")

    class Meta(ProductSerializer.Meta):
        exclude = [
            'category',
            'main_colour',
            'second_colour',
            'logo_colour',
            'brand',
            'inclusion_date',
            'url_img',
            'initial_stock',
            'current_stock',
            'size',
            'sizing',
            'fabric',
            'sleeve',
        ]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = CartItem
        fields = ["id", "cart", "product", "quantity", "sub_total"]

    def total(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.price


class AddCartItemSerializer(CartItemSerializer):
    product_id = serializers.UUIDField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product associated with the given ID")

        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]
        product = Product.objects.filter(id=product_id)
        try:
            if product.is_available:
                cart_item = CartItem.objects.get(
                    product_id=product_id,
                    cart_id=cart_id
                )
                cart_item.quantity += quantity
                cart_item.save()

                self.instance = cart_item
            else:
                raise ValidationError("This product is out of stock")
        except:
            self.instance = CartItem.objects.create(
                cart_id=cart_id,
                **self.validated_data
            )
        finally:
            #  Stock update
            product.current_stock -= quantity
            product.save()

        return self.instance

    class Meta(CartItemSerializer.Meta):
        fields = ["id", "product_id", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    total = serializers.SerializerMethodField(method_name='main_total')
    items = serializers.SerializerMethodField(method_name='cart_items')

    class Meta:
        model = Cart
        fields = ["id", "items", "total", "created", "completed"]

    def main_total(self, cart_item: CartItem):
        total = CartItem.objects.filter(cart=cart_item.id).select_related('product').values_list(
            'product__price').aggregate(
            Sum('product__price'))
        return total['product__price__sum']

    def cart_items(self, cart_item: CartItem):
        items = CartItem.objects.filter(cart=cart_item.id).select_related('product').values('product__id',
                                                                                            'product__description',
                                                                                            'product__price')
        return items


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
