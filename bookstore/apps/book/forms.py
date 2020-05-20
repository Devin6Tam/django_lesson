#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        min_length=4,
        max_length=30,
        error_messages={
            "required":"不能为空",
            "invalid":"格式错误",
            "min_length":"用户名最短为4位"
        },
        label="名字"
    )
    email = forms.EmailField(required=False, label="邮箱")
    message = forms.CharField(widget=forms.Textarea, label="留言")