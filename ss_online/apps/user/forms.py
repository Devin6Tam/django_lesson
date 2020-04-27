from django import forms


class LoginForm(forms.Form):
    #  需要校验的字段，一定要跟前端中的name属性对应
    username = forms.CharField(required=True, min_length=3, max_length=30)
    password = forms.CharField(required=True, min_length=6)
