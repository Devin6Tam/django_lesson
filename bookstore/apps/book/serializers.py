#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/21 23:31
# @Author  : tanxw
# @Desc    : books 序列化使用
from rest_framework import serializers

from .models import BookInfo


class BookRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        """自定义用于处理图书的字段"""
        return "图书的名字是：%s,图书的ID：%d" % (value.btitle, value.id)

# class BookInfoSerializer(serializers.ModelSerializer):
#     """图书的数据序列化器"""
#     class Meta:
#         model = BookInfo
#         # fields = "__all__"
#         fields = ('id','btitle')

class BookInfoSerializer(serializers.Serializer):
    """图书的数据序列化器"""
    id = serializers.IntegerField(label="ID", read_only=True) #只读 只做序列化的输出
    btitle = serializers.CharField(max_length=20, label="名称")
    # bpub_date = serializers.DateField(label="发布日期")
    bread = serializers.IntegerField(label="阅读量")
    bcomment = serializers.IntegerField(label="评论量")
    # is_delete = serializers.BooleanField(default=False, label="逻辑删除")
    # image = serializers.ImageField(required=False, label="封面图片")
    # heroinfo_set = serializers.StringRelatedField(read_only=True, many=True)
    heros = serializers.StringRelatedField(read_only=True, many=True)

    def validate_btitle(self, value):
        # 对特定指定的字段进行单独的辅助的校验方法
        if 'ad' in value.lower():
            raise serializers.ValidationError("不能含有广告词汇！！！")
        return value

    def validate(self, value):
        bread = value['bread']
        bcomment = value['bcomment']
        if bread < bcomment:
            raise serializers.ValidationError('阅读量小于评论量')
        return value


    def update(self, instance, validated_data):
        """更新数据"""
        instance.btitle = validated_data.get('btitle', instance.btitle)
        instance.bpub_date = validated_data.get('bpub_date', instance.bpub_date)
        instance.bread = validated_data.get('bread', instance.bread)
        instance.bcomment = validated_data.get('bcomment', instance.bcomment)
        instance.save()
        return instance

    def create(self, validated_data):
        """新增数据"""
        book = BookInfo(**validated_data) # 字典的解包
        book.save()
        return book

