from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    #  需要校验的字段，一定要跟前端中的name属性对应
    username = forms.CharField(required=True, min_length=3, max_length=30)
    password = forms.CharField(required=True, min_length=6)


class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, max_length=11, min_length=11)
    captcha = CaptchaField(required=True, error_messages={'invalid': "验证码错误"})

class SmsCodeForm(forms.Form):
    mobile = forms.CharField(max_length=11, min_length=11, required=True)
    captcha = CaptchaField(required=True, error_messages={'invalid': "验证码错误"})