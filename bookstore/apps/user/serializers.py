#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/24 21:59
# @Author  : tanxw
# @Desc    : 用户模块序列化器
import re

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    用户注册的序列化器
    """
    # {"mobile": "13838383838", "password": "132456", "password2": "123456"}
    password2 = serializers.CharField(label="重复密码", max_length=16, required=True, write_only=True)

    class Meta:
        model = User
        fields = ("id", "mobile", "password", "password2")

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9][0-9]{9}', value):
            print(value)
            raise serializers.ValidationError("手机号码格式错误！")
        return value

    def validate(self, data):
        print(data)
        if data["password2"] != data["password"]:
            raise serializers.ValidationError("两次输入的密码不一致")
        return data

    def create(self, validated_data):
        print(validated_data)
        del validated_data["password2"]
        print(validated_data)
        # User.objects.create(mobile=validated_data["mobile"], password=validated_data["password"])
        user = User(**validated_data)  # 字典的解包
        user.save()
        return user



