from django.contrib import admin
from products.models import *
# Register your models here.
admin.site.register(Category),
admin.site.register(ColorVariant),
admin.site.register(SizeVariant),
admin.site.register(Product),
admin.site.register(ProductImage),
admin.site.register(Coupon),
admin.site.register(ProductReview),
admin.site.register(Wishlist),