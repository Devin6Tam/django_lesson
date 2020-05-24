from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView

from .models import User
from .serializers import UserSerializer


# 注册
class RegView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
