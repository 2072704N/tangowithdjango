from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<HTML> Rango says hey there world! <a href='http://127.0.0.1:8000/rango/about/'> about page </a></HTML>")

def about(request):
    return HttpResponse("<HTML> Rango says here is the about page.----- This tutorial has been put together by Callum Nixon, 2072704N <a href='http://127.0.0.1:8000/rango/'> index page </a></HTML>")
