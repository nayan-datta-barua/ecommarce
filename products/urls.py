from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('product-detail/',ProductDetailView.as_view()),
    path('product-review/',ProductReviewView.as_view()),
    path('wish/',WishlistView.as_view()),
    path('add-wish/',AddToWishlistView.as_view()),
]
