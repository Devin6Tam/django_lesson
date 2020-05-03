#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/4 0:11
# @Author  : tanxw
# @Desc    : 描述使用说明
from django import forms
from apps.operation.models import UserAsk

class AddAskForm(forms.ModelForm):
    # ModelForm 可以直接与model相关联；如果定义为forms.Form，需要自己重新定义字段
    mobile = forms.CharField(min_length=11, max_length=11, required=True)
    class Meta:
        # 采用的model名称
        model = UserAsk
        # form中有model的哪些字段，__all__ 代表着所有字段
        # fields = '__all__'
        fields = ['mobile', 'name', 'course_name']
        # 不需要哪些字段
        # exclude = ['add_time']
