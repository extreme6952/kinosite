from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox  
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=75)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,
                               label='Придумайте пароль',
                               required=True)
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label='Введите пароль ещё раз',
                                required=True)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
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

