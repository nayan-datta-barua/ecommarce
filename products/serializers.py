from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, ColorVariant, SizeVariant, Product, ProductImage, Coupon, ProductReview, Wishlist

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'slug', 'category_image']

class ColorVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorVariant
        fields = ['id', 'color_name', 'price']

class SizeVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeVariant
        fields = ['id', 'size_name', 'price', 'order']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    color_variant = ColorVariantSerializer(many=True)
    size_variant = SizeVariantSerializer(many=True)
    product_images = ProductImageSerializer(many=True, source='product_images')

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'slug', 'category', 'price', 'product_desription', 'color_variant', 'size_variant', 'newest_product', 'product_images', 'get_rating']

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'coupon_code', 'is_expired', 'discount_amount', 'minimum_amount']

class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'user', 'stars', 'content', 'date_added']

class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    size_variant = SizeVariantSerializer()

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'size_variant', 'added_on']
        extra_kwargs = {
            'user': {'write_only': True},
        }
