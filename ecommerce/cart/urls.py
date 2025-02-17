"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from cart import views
app_name="cart"

urlpatterns = [
    path('addtocart/<int:i>/',views.addtocart,name='addtocart'),
    path('cartview',views.cartview,name='cartview'),
    path('cartdecrement/<int:pk>',views.cart_decrement,name='cartdecrement'),
    path('cart_delete/<int:pk>',views.cart_delete,name="cartdelete"),
    path('order_form',views.order_form,name="orderform"),
    path('status/<str:n>/',views.status,name="status"),
    path('order_view',views.order_view,name="orderview"),
]

