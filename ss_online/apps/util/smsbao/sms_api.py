#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/30 0:19
# @Author  : tanxw
# @Desc    : 短信宝api

import urllib
import urllib.request
import hashlib

def md5(str):
    # import hashlib
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

status_str = {
    '0': '短信发成功',
    '-1': '参数不全',
    '-2': '服务器空间不支持，请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
    '30': '密码错误',
    '40': '账号不存在',
    '41': '账号余额不足',
    '50': '内容含有敏感词'
}
def sms_send_message(phone,code):
    smsapi = 'http://api.smsbao.com/'
    # 短信平台账号
    user = 'tanxw'
    # 短信平台密码
    # password = md5('xxxxxx')
    # print(password)
    password = 'dc483e80a7a0bd9ef71d8cf973673924'
    # 要发送的短信内容
    content = '您的验证码是{},5分钟内有效.若非本人操作请忽略此消息。'.format(code)
    # 要发送的短信手机号码
    # phone = 'XXXXXXXXXX'

    data = urllib.parse.urlencode({'u': user,'p': password, 'm': phone, 'c': content})
    send_url = smsapi + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read().decode('utf8')
    print(status_str[the_page])
    return the_page

if __name__ == '__main__':
    sms_send_message('18898750918', '561436')