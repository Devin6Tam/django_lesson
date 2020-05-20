import json
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from .models import BookInfo
from .forms import ContactForm


class BookAPIView(View):
    """单个图书的操作"""

    def get(self, request, pk):
        """
        获取单个图书信息
        路由： GET  /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

    def put(self, request, pk):
        """
        修改图书信息
        路由： PUT  /books/<pk>
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)
        print(book_dict)

        # 此处详细的校验参数省略

        book.btitle = book_dict.get('btitle')
        book.bpub_date = datetime.strptime(book_dict.get('bpub_date'), '%Y-%m-%d').date()
        book.save()

        return JsonResponse({
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
            'bread': book.bread,
            'bcomment': book.bcomment,
            'image': book.image.url if book.image else ''
        })

    def delete(self, request, pk):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(pk=pk)
        except BookInfo.DoesNotExist:
            return HttpResponse(status=404)

        book.delete()

        return HttpResponse(status=204)


class BooksApiView(View):
    """对图书的查询和增加"""

    def get(self, request):
        # 查询所有图书
        queryset = BookInfo.objects.all()
        book_list = []
        for book in queryset:
            book_list.append({
                'id': book.id,
                'btitle': book.btitle,
                'bpub_date': book.bpub_date,
                'image': book.image.url if book.image else ''
            })
            # 三元表达式
        return JsonResponse(book_list, safe=False)

    def post(self, request):
        # 新增图书
        json_bytes = request.body
        json_str = json_bytes.decode("utf8")
        book_dict = json.loads(json_str, encoding="utf8")

        b = BookInfo.objects.create(
            btitle=book_dict.get('btitle'),
            bpub_date=book_dict.get('bpub_date'),
            image=''
        )
        book = {'id': b.id, 'btitle': b.btitle, 'bpub_date': b.bpub_date}
        return JsonResponse(book)


# {"btitle":"西游记","bpub_date":"2020-5-15"}

def reg(request):
    """注册页面"""
    error_msg = ""
    if request.method == "POST":
        username = request.POST.get("name")
        pwd = request.POST.get("pwd")

        # 校验
        if len(username) < 6:
            # 用户的注册名字小于6位
            error_msg = "用户名长度不能小于6位"
        else:
            # 讲用户名和密码存到数据库 ORM
            # try:
            #     Users.objects.create(name=username,password=pwd)
            #     .....
            # user = Users.objects.get(name=username)
            # if pwd == user.password:
            # else:
            #     pass

            return HttpResponse("注册成功")

    return render(request, "reg.html", {'error_messages': error_msg})


class ContactUs(View):
    """留言"""

    def get(self, request):
        form = ContactForm(initial={'name': '匿名'})
        return render(request, 'cantact_form.html', {'form': form})

    def post(self, request):
        form = ContactForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            print(form.cleaned_data.get('name'))
            print(form.cleaned_data.get('email'))
            print(form.cleaned_data.get('message'))

            # 保存到数据库里进行留言 ORM
            # Contact.objects.create(name=name,email=form.cleaned_data.get('email').....)
            return HttpResponse("提交成功")
        else:
            print(form.errors)
            return HttpResponse("提交失败")
