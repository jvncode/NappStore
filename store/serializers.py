from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Category, Product, Cart, CartItems, Customer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "category",
            "main_colour",
            "second_colour",
            "logo_colour",
            "brand",
            "inclusion_date",
            "url_img",
            "price",
            "initial_stock",
            "current_stock",
            "description",
        ]


class TShirtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "category",
            "main_colour",
            "second_colour",
            "brand",
            "inclusion_date",
            "url_img",
            "price",
            "initial_stock",
            "current_stock",
            "description",
            "size",
            "sizing",
            "fabric",
            "sleeve",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source="category.name")

    class Meta:
        model = Product
        exclude = ['initial_stock']

    def get_caps(self, obj):
        if obj.category.name == "cap":
            return CapSerializer(obj)

    def get_tshirts(self, obj):
        if obj.category.name == "tshirt":
            return TShirtSerializer(obj)


class SimpleProductSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source="category.name")
    class Meta:
        model = Product
        fields = ["id", "category_name", "description", "price"]


class CartItemsSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(many=False)
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = CartItems
        fields = ["id", "cart", "product", "quantity", "sub_total"]

    def total(self, cart_item: CartItems):
        return cart_item.quantity * cart_item.product.price


class AddCartItemSerializer(serializers.ModelSerializer):
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
                cart_item = CartItems.objects.get(
                    product_id=product_id,
                    cart_id=cart_id
                )
                cart_item.quantity += quantity
                cart_item.save()

                self.instance = cart_item
            else:
                raise ValidationError("This product is out of stock")
        except:
            self.instance = CartItems.objects.create(
                cart_id=cart_id,
                **self.validated_data
            )
        finally:
            #  Stock update
            product.current_stock -= quantity
            product.save()

        return self.instance

    class Meta:
        model = CartItems
        fields = ["id", "product_id", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemsSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(method_name='main_total')

    class Meta:
        model = Cart
        fields = ["id", "items", "total", "created", "completed"]

    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'