from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, RetrieveUpdateAPIView

from .models import Product, Category, Cart, CartItem, Customer
from .serializers import CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, \
    AddCartItemSerializer, CustomerSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet, RetrieveAPIView):
    queryset = Product.objects.all().order_by('category')
    serializer_class = ProductSerializer


class ProductUpdate(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDelete(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(viewsets.ModelViewSet, RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartUpdate(RetrieveUpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer

        return CartItemSerializer

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_pk"]}


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
