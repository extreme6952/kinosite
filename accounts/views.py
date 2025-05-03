from django.http.response import HttpResponseRedirect
from .forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views.generic.base import View,TemplateResponseMixin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.views.generic.base import TemplateView

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
            user:User = form.save()
            user.is_active = False
            user.save()
            return HttpResponseRedirect(reverse_lazy('account:signup_done'))
        else:
            messages.error(request,'Произошла неизвестная ошибка,повторите попытку позже')
        return self.render_to_response({'form':form,})
    
class CustomRegistrationDoneView(TemplateView):
    template_name = 'registration/signup_done.html'