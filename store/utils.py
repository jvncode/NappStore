from django.core.mail import send_mail
from django.conf import settings

from .models import Cart, CartItems
from .serializers import CartItemsSerializer


def send_mail_customer(customer_cart):
    cart = Cart.objects.filter(id=customer_cart.id).first()
    purchase = CartItems.objects.filter(cart=cart.id).first()
    items = CartItemsSerializer(purchase).data
    message = f"You have made a purchase of {items['sub_total']}€."
    send_mail(
        subject="The summary of your purchase",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[customer_cart.email]
    )
