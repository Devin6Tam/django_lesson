from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponse
from .models import UserProfile
from .forms import LoginForm
from django.contrib.auth import authenticate, login
# Create your views here.

class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # username = request.POST.get('username')
            # password = request.POST.get('password')
            print((username, password))
            #  验证用户是否存在
            user = authenticate(username=username, password=password)
            # user = UserProfile.objects.filter(username=username, password=password)
            if user:
                #  登录的操作，实际上是配置cookie和sessionid
                login(request, user=user)
                # return HttpResponse('OK!')
                #  不会产生url的变化
                # return render(request, 'index.html')
                return redirect(reverse('index'), {'request': request})
            else:
                return HttpResponse('invalid password')
        else:
            return render(request, 'login.html', {'form': login_form})
