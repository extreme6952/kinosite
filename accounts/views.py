from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views.generic.base import View,TemplateResponseMixin


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