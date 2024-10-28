from django.contrib import admin
from django.urls import path,include
from card.views import *

urlpatterns = [

    path('item-detail/',CartDetailView.as_view()),
    path('item-add/',CartItemAddView.as_view()),
    path('cart/',CartItemRemoveView.as_view()),
    path('order-list/',OrderListView.as_view()),
    path('order-detail/',OrderDetailView.as_view()),
    path('create-order/',CreateOrderView.as_view()),
    path('ship-addredd/',ShippingAddressListView.as_view()),

    path('ship-detail/',ShippingAddressDetailView.as_view()),
    path('shio-update/',ShippingAddressUpdateView.as_view()),
]
