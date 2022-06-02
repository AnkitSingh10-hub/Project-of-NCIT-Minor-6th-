from django.contrib import admin
from .models import Category, SubCategory, Product, Carousel, Cart, Brand
# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Carousel)
admin.site.register(Cart)
admin.site.register(Brand)