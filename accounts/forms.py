from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=75)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,
                               required=True)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                required=True)
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email',]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароль не совпадает')    
        return cd['password2']
    
    def clean_email(self):
        data = self.cleaned_data["email"]
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Данный email уже зарегстрирован')
        return data