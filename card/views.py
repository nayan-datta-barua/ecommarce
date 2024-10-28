from django.shortcuts import render
from products.models import *
from  users.models import *

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# from account.serializers import *
from django.shortcuts import get_object_or_404
from products.serializers import *
from users.serializers import *
from card.serializers import *


# Cart Views
class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user, is_paid=False)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user, is_paid=False)
        data = request.data.copy()
        data['cart'] = cart.id
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        """
        Full update (PUT) for a CartItem.
        Updates all fields of the CartItem instance with the provided data.
        """
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partial update (PATCH) for a CartItem.
        Updates only the provided fields of the CartItem instance.
        """
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user, cart__is_paid=False)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Order Views
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user, is_paid=False)
        data = request.data.copy()
        data['user'] = request.user.id
        data['order_total_price'] = cart.get_cart_total_price_after_coupon()
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            cart.is_paid = True
            cart.save()  # Mark the cart as paid after creating an order
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
            """
            Delete an order that belongs to the authenticated user.
            """
            # Ensure the order belongs to the current user
            order = get_object_or_404(Order, pk=pk, user=request.user)
            
            # Perform the delete operation
            order.delete()
            return Response({"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


# Shipping Address Views
class ShippingAddressListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = CustomUser.objects.filter(user=request.user)
        serializer = UserSerializer(addresses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShippingAddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        address = get_object_or_404(CustomUser, pk=pk, user=request.user)
        serializer = UserSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        address = get_object_or_404(CustomUser, pk=pk, user=request.user)
        serializer = UserSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        address = get_object_or_404(CustomUser, pk=pk, user=request.user)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class ShippingAddressUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        """
        Updates the shipping address with the given `pk`.
        Full update (PUT) of the shipping address.
        """
        address = get_object_or_404(CustomUser, pk=pk, user=request.user)
        serializer = UserSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Partially updates the shipping address with the given `pk`.
        """
        address = get_object_or_404(CustomUser, pk=pk, user=request.user)
        serializer = UserSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)