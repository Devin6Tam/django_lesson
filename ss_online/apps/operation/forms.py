#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/5 18:10
# @Author  : tanxw
# @Desc    : form 表单数据处理
from django import forms
from .models import UserFavorite, CourseComments


# 添加收藏表单
class AddFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ['fav_id', 'fav_type']


# 添加评论
class AddCommentForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        # 注意虽然前端传过来的course_id,但会自动转成course对象
        fields = ['course', 'comments']

