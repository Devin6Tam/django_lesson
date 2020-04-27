#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 23:57
# @Author  : tanxw
from .models import Citys
from import_export import resources

class CityResource(resources.ModelResource):

    class Meta:
        model = Citys
        # 导入数据时，如果该条数据未修改过，则会忽略
        skip_unchanged = True
        # 在导入预览页面中显示跳过的记录
        report_skipped = True
        # 对象标识的默认字段是id，您可以选择在导入时设置哪些字段用作id
        import_id_fields = ('id',)
        # 白名单
        fields = ('id', 'name', 'desc',)
        # 黑名单
        exclude = ('add_time',)
