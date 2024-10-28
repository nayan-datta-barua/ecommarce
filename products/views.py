from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
import random
from products.serializers import *
from products.models import *




# class CategoryView(APIView):
#     def get(self,request):
#         cate = Category.objects.all()
#         seri= CategorySerializer(cate,many=True)
#         return Response(seri.data)
# class CategoryView(APIView):
#     def get(self,request):
#         cate = ColorVariant.objects.all()
#         seri= ColorVariantSerializer(cate,many=True)
#         return Response(seri.data)
# class CategoryView(APIView):
#     def get(self,request):
#         cate = Category.objects.all()
#         seri= CategorySerializer(cate,many=True)
#         return Response(seri.data)

class ProductDetailView(APIView):
    def get(self, request, slug):
        product = Product.objects.get(Product, slug=slug)
        serializer = ProductSerializer(product)
        
        # Serialize the product data
        return Response(serializer.data)

    def post(self, request, slug):
        product = Product.objects.get(Product, slug=slug)

        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            review = ProductReview.objects.get(product=product, user=request.user)
            serializer = ProductReviewSerializer(review, data=request.data)
        except ProductReview.DoesNotExist:
            serializer = ProductReviewSerializer(data=request.data)

        if serializer.is_valid():
            review = serializer.save(user=request.user, product=product)
            return Response({"message": "Review added successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        try:
            review = ProductReview.objects.get(product=product, user=request.user)
            review_serializer = ProductReviewSerializer(instance=review, data=request.data)
        except ProductReview.DoesNotExist:
            review_serializer = ProductReviewSerializer(data=request.data)
        
        if review_serializer.is_valid():
            review = review_serializer.save(user=request.user, product=product)
            return Response({"message": "Review added successfully!"}, status=status.HTTP_201_CREATED)
        
        return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class WishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist_items = Wishlist.objects.filter(user=request.user)
        serializer = WishlistSerializer(wishlist_items, many=True)
        
        # Return serialized wishlist data
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class AddToWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uid):
        variant = request.GET.get('size')
        if not variant:
            return Response({"error": "Please select a size before adding to the wishlist!"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, uid=uid)
        size_variant = get_object_or_404(SizeVariant, size_name=variant)
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product, size_variant=size_variant)

        serializer = WishlistSerializer(wishlist)

        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "Product already in Wishlist"}, status=status.HTTP_200_OK)
    



