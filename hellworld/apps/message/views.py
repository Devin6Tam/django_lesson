from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import MessageInfo
from django.views import View
# Create your views here.
def index(request):
    return render(request, 'message/message_form.html')

# 代表该函数取消csrf认证
@csrf_exempt
def submit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        message = request.POST.get("message")
        print((name, email, address, message))
        messageInfo = MessageInfo()
        messageInfo.name = name
        messageInfo.email = email
        messageInfo.address = address
        messageInfo.message = message
        messageInfo.save()
        return JsonResponse({"msg": "OK"})
    else:
        return JsonResponse({"msg": "requests error"})

def student(request):
    pass


class CBV_Message_Submit_View(View):
    def get(self, request):
        return render(request, 'message/message_form.html')

    def post(self, request):
        return JsonResponse({"msg": "requests error"})
