from rest_framework import serializers
from django.contrib.auth.models import User
from card.models import *
from products.serializers import *
from users.serializers import *



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    color_variant = ColorVariantSerializer(read_only=True)
    size_variant = SizeVariantSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'color_variant', 'size_variant', 'quantity', 'get_product_price']


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    cart_items = CartItemSerializer(many=True, read_only=True)
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'cart_items', 'coupon', 'is_paid', 'razorpay_order_id', 'razorpay_payment_id', 
                  'razorpay_payment_signature', 'get_cart_total', 'get_cart_total_price_after_coupon']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    size_variant = SizeVariantSerializer(read_only=True)
    color_variant = ColorVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'size_variant', 'color_variant', 'quantity', 'product_price', 'get_total_price']


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    coupon = CouponSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_id', 'order_date', 'payment_status', 'shipping_address', 'payment_mode', 
                  'order_total_price', 'coupon', 'grand_total', 'order_items', 'get_order_total_price']

