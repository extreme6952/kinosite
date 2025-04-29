from .forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views.generic.base import View,TemplateResponseMixin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm


#Временное решение в качестве аналога аутентификации юзера - 
# - Тестирую добавление капчи 
class UserLoginView(TemplateResponseMixin,View):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return self.render_to_response({'form':form,
                                        'error':''})
    
    def post(self,request):
        form = self.form_class(request.POST)
        error = ''
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('list_series')
                else:
                    error = 'Аккаунт отключён'
            else:
                error = 'Неверный логин или пароль'
        return self.render_to_response({'form':form,
                                        'error':error,})
    
class UserRegistrationView(TemplateResponseMixin,View):
    template_name = 'registration/registration_template.html'
    form_class = UserRegistrationForm
    
    def get(self,request):
        form = self.form_class()
        return self.render_to_response({'form':form})
    
    def post(self,request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.success(request,'Вы успешно зарегестрировались')
            return redirect('account:login')
        else:
            messages.error(request,'Произошла неизвестная ошибка,повторите попытку позже')
        return self.render_to_response({'form':form,})
    