from django.http.response import HttpResponseRedirect
from .forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.views.generic.base import View,TemplateResponseMixin
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse_lazy
from .tasks import activate_email_task

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
            activate_email_task.delay(user_id=user.pk)
            return HttpResponseRedirect(reverse_lazy('account:signup_done'))
        else:
            messages.error(request,'Произошла неизвестная ошибка,повторите попытку позже')
        return self.render_to_response({'form':form,})
    
class CustomRegistrationDoneView(TemplateView):
    template_name = 'registration/signup_done.html'

class CustomRegistrationConfirmView(View):
    def get(self,request,uidb64,token):
        try:
            # uid юзера преобразуем в int по его id (раскодируем его id)
            uid = urlsafe_base64_encode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError,ValueError,OverflowError,User.DoesNotExist):
            user = None
        #Проверка,что юзер такой имеется и проверятеся,что токен,который 
        #для него создавался тоже такой есть
        if user is not None and default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            login(request,user)
            return render(request,
                          'registration/signup_user_confirm.html',
                          {'title':'Учётная запись успешно активирована'})
        else:
            return render(
                request,
                'registration/signup_user_error.html',
                {'title':'Произошла ошибка при подтверждении аккаунта'}
            )
