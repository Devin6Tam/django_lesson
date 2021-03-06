"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views
from .views import BookInfoViewSet

urlpatterns = [
    path('reg/', views.reg),
    re_path(r'^contact/$', views.ContactUs.as_view()),
    # re_path(r'^books/$', views.BooksApiView.as_view()),
    re_path(r'^test/$', views.ApiTestView.as_view()),
    # re_path(r'^books/(?P<pk>\d+)/$', views.BookAPIView.as_view()),
]

# drf可以出来视图的路由器
router = DefaultRouter()
router.register(r'books', BookInfoViewSet)
# print(router.urls)
urlpatterns += router.urls
