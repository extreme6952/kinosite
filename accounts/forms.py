from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(max_length=75)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()