from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('master/', views.Master, name='master'),
    path('', views.Index, name='index'),

    # adding url for authentication system
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="login"),
    path('signout/', views.signout, name="signout"),
    # url for cart
    path('add-to-cart/', views.add_to_cart, name="add-to-cart"),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name="remove-cart"),
    path('cart/', views.cart, name="cart"),
    path('plus-cart/<int:cart_id>/', views.plus_cart, name="plus-cart"),
    path('minus-cart/<int:cart_id>/', views.minus_cart, name="minus-cart"),
    #product page
    path('product/', views.Product_page, name="product"),
    path('product/<str:id>', views.Product_Detail, name="product_detail"),
    #search
    path('search/', views.Search, name="search"),
    #contact
    path('contact/', views.Contact, name="contact"),
]
