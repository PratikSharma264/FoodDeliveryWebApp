from django.shortcuts import render
from django.http import HttpResponse


def home_view(request):
    return HttpResponse("init Food Delivery App Home Page")
