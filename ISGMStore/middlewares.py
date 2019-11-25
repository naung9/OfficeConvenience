'''
Created on Mar 1, 2019

@author: naung9
'''
from django.shortcuts import redirect,reverse
from django.contrib.auth.models import User


class AuthRequiredMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # print(request.path)
        # print("Determining Whether User is logged in")
        # is_not_allowed = reverse('ISGMStore:login') not in request.path and reverse("admin:login") not in request.path and reverse('ISGMStore:register') not in request.path
        # if is_not_allowed or request.path == "/store/" or request.path == "/":
        #     print("User Is Accessing To Other Pages")
        #     if not request.user.is_authenticated and type(request.user) != User:
        #         print("Redirecting To Login Page")
        #         return redirect(reverse('ISGMStore:login'))
        # if not request.user.is_authenticated and type(request.user) != User and is_not_allowed:
        #     return redirect(reverse('ISGMStore:login')) # or http response
        response = self.get_response(request)
        # print("Redirecting To Deisred Page")
        return response
