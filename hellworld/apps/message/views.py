from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    return render(request, 'message/message_form.html')

# 代表该函数取消csrf认证
@csrf_exempt
def submit(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    address = request.POST.get("address")
    message = request.POST.get("message")
    print(name, email, address, message)
    return JsonResponse({"msg": "OK"})

def student(request):
    pass