from django.core.mail import send_mail
from django.conf import settings

from .models import Cart, CartItem
from .serializers import CartItemSerializer


def send_mail_customer(customer_cart):
    cart = Cart.objects.filter(id=customer_cart.id).first()
    purchase = CartItem.objects.filter(cart=cart.id).first()
    items = CartItemSerializer(purchase).data
    message = f"You have made a purchase of {items['sub_total']}€."
    send_mail(
        subject="The summary of your purchase",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[customer_cart.email]
    )
