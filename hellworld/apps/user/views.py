from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse


def index(request):
    return render(request, 'user/index.html', {'h1': 'hello'})

def abc(request):
    return HttpResponse("abc")


def hello(request):
    # A.反解析（逆向）及重定向
    return redirect(reverse('user:abc'))
    # B.反解析（逆向）及重定向
    # return redirect('users:abc')
    # C.反解析（逆向）及重定向
    # return HttpResponseRedirect(reverse('users:abc'))