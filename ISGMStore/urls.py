'''
Created on Feb 27, 2019

@author: naung9
'''
from django.urls import path
from django.contrib.auth.views import auth_login
from . import views

app_name = "ISGMStore"
urlpatterns = [
    path('',views.index,name="index"),
    path('category/<int:id>',views.category,name="category"),
    path('checkout',views.checkout,name="checkout"),
    path('confirm_checkout',views.confirm_checkout,name="confirm_checkout"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('user_profile',views.user_profile,name="user_profile"),
    path('register',views.register,name="register"),
    path('invoices',views.invoices,name="invoices"),
    path('invoice/<int:pk>',views.invoice,name="invoice"),
    ]
