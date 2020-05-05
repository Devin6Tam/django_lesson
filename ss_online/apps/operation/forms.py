#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/5 18:10
# @Author  : tanxw
# @Desc    : form 表单数据处理
from django import forms
from .models import UserFavorite

class AddFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ['fav_id', 'fav_type']

