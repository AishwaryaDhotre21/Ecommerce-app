from django.contrib import admin
from django.urls import path
from .views import Index
from .views import signup
from .views import login,logout,cart_page,Checkout
from .views import orders_view
urlpatterns = [
   path('',Index.as_view(),name='homepage'),
   path('signup',signup,name='signuppage'),
   path('login',login.as_view(),name='loginpage'),
   path('logout',logout,name='logoutpage'),
   path('cart',cart_page.as_view(),name='cartpage'),
   path('checkout',Checkout.as_view(),name='checkoutpage'),
   path('orders',orders_view.as_view(),name='orderspage')
]