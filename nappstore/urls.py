"""nappstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from store.views import CategoryViewSet, ProductViewSet, CartViewSet, ProductDelete, ProductUpdate, CartUpdate, CustomerViewSet

router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'product', ProductViewSet)
router.register(r'product/<int:pk>', ProductViewSet)
router.register(r'carts', CartViewSet)
router.register(r'carts/<str:pk>', CartViewSet)
router.register(r'customers', CustomerViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('cart/<str:pk>/update', CartUpdate.as_view()),
    path('product/<int:pk>/delete', ProductDelete.as_view()),
    path('product/<int:pk>/update', ProductUpdate.as_view()),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += router.urls
