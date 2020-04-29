from django import forms
from captcha.fields import CaptchaField
from django.conf import settings
import redis
from django.contrib.auth import get_user_model

UserProfile = get_user_model()
class LoginForm(forms.Form):
    #  需要校验的字段，一定要跟前端中的name属性对应
    username = forms.CharField(required=True, min_length=3, max_length=30)
    password = forms.CharField(required=True, min_length=6)


class DynamicLoginForm(forms.Form):
    """验证码的展示及正确性校验"""
    mobile = forms.CharField(required=True, max_length=11, min_length=11)
    captcha = CaptchaField(required=True, error_messages={'invalid': "验证码错误"})


"""登录，注册都将会用到这些重复的属性，方法，所以做成基础类，便于简洁代码"""
class BaseUserForm(forms.Form):
    mobile = forms.CharField(max_length=11, min_length=11, required=True)
    code = forms.CharField(max_length=6, min_length=6, required=True)

    def clean_code(self):
        # 创建redis连接
        redis_conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                                 db=settings.REDIS_DB, encoding='utf8')
        # 获取用户输入的手机号码
        recv_mobile = self.data.get('mobile')
        # 获取用户输入的短信验证码
        recv_code = self.data.get('code')

        print('recv_mobile', recv_mobile, type(recv_mobile))
        # 从redis库中获取缓存的短信验证码
        store_code = redis_conn.get(recv_mobile).decode()
        if recv_code == store_code:
            return self.cleaned_data
        raise forms.ValidationError('短信验证码错误！')


class SmsCodeForm(BaseUserForm):
    """用户使用动态登录的时候，进行数据校验，在redis 查询验证码"""
    pass

class RegisterForm(BaseUserForm):
    password = forms.CharField(max_length=20, min_length=6, required=True)

    def clean_mobile(self):
        mobile = self.data.get('mobile')
        user = UserProfile.objects.filter(username=mobile)
        if user:
            raise forms.ValidationError('手机号已经存在')
        return mobile