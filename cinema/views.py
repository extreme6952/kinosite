from django.views.generic.detail import DetailView
from .forms import *
from .models import *
from django.apps import apps
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.forms.models import modelform_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View,TemplateResponseMixin
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login


class UserMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
    
class UserEditFormMixin:
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class UserSeriesMixin(UserMixin,
                      LoginRequiredMixin,
                      TemplateResponseMixin,):
    model = Series
    fields = ['name','cover','description','studio']
    success_url = reverse_lazy('list_user_series')

class DeleteSeriesUser(UserSeriesMixin,DeleteView):
    template_name = 'series/series_redaction_user/delete_series.html'



class UserSeriesEditMixin(UserEditFormMixin,UserSeriesMixin):
    template_name = 'series/series_redaction_user/form_add_series.html'

class SeriesAddFormView(TemplateResponseMixin,View):
    template_name = 'series/series_redaction_user/form_add_series.html'

    def get_form(self,data=None,files=None,*args, **kwargs):
        return AddSeriesUser(data=data,files=files)

    def get(self,request):
        form = self.get_form()
        return self.render_to_response({'form':form})
    
    def post(self,request):
        form = self.get_form(data=request.POST,files=request.FILES)
        if form.is_valid():
            series = form.save(commit=False)
            series.user = request.user
            series.save()
            messages.success(request,'Вы успешно добавили новые данные!')
            return redirect('list_user_series')
        else:
            messages.error(request,'Произошла ошибка, повторите попытку')
        return self.render_to_response({'form':form})
    

    
class SeriesUserListView(UserSeriesMixin,ListView):
    template_name = 'series/series_redaction_user/list_series_user.html'

class AddSeasonSeriesView(TemplateResponseMixin,View):
    template_name = 'series/series_redaction_user/list_series_user.html'
    series = None

    def dispatch(self, request, pk ,*args, **kwargs):
        self.series = get_object_or_404(Series,
                                        id=pk,
                                        user=request.user)
        
        return super().dispatch(request,pk,*args, **kwargs)
     
    def get(self,request,pk):
        return self.render_to_response({'series':self.series,})
    
    def post(self,request,pk):
        season = Season.objects.create(series=self.series)
        return redirect('series_season_user',season.pk)
    
# Запрос приходит на URL, связанный с этим представлением. Например:
# /courses/module/1/content/text/2/, где:
# 1 — это module_id (идентификатор модуля),
# text — это model_name (тип содержимого),
# 2 — это id объекта содержимого (если есть).
class VideoSeriesSeasonCreateUpdateView(TemplateResponseMixin,View):
    template_name = 'series/series_redaction_user/form_create_update_video.html'
    #Модель данных, с которой работает представление 
    #(например, Text, Video, Image, File).
    model = None
    #Объект модуля, к которому относится содержимое.
    season = None
    #Объект содержимого модуля (например, текст, видео, изображение или файл).
    obj = None

    # Этот метод возвращает модель данных на основе переданного имени модели (model_name). 
    # Он проверяет, принадлежит ли model_name одному из допустимых типов 
    # содержимого (text, video, image, file). Если да, 
    # то он возвращает соответствующую модель из приложения courses. 
    # Если нет, возвращает None
    def get_model(self,model_name):
        if model_name in ['video']:
            return apps.get_model(app_label='cinema',
                                  model_name=model_name)
        return None
    
    # Создаем форму на основе модели, 
    # исключая поля 'owner', 'created', 'updated', 'order'.
    def get_form(self,model,*args, **kwargs):
        Form = modelform_factory(model,
                                 exclude=['user',
                                          'created',
                                          'updated',])        
        return Form(*args, **kwargs)
    
    #Загружаем объект модуля по module_id. 
    #Если модуль не найден или курс не принадлежит пользователю, возвращаем 404.
    def dispatch(self, request,season_id,model_name,id=None,):
        self.season = get_object_or_404(Season,
                                        id=season_id,
                                        series__user=request.user)
        # Определяем модель данных на основе model_name.
        self.model = self.get_model(model_name)
        # Если передан id, то загружается объект содержимого модуля.
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         user=request.user)        
        return super().dispatch(request,season_id,model_name,id)
    
    #Этот метод обрабатывает GET-запросы. Он создает форму для редактирования 
    #объекта содержимого (если он существует) и передает её в шаблон для отображения.
    def get(self,request,season_id,model_name,id=None):
        form = self.get_form(self.model,
                             instance=self.obj)    
        return self.render_to_response({'form':form,
                                        'object':self.obj,
                                        'season':self.season,
                                        'series':self.season.series})
    
    def post(self,request,season_id,model_name,id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        # Создаем форму с данными из POST-запроса и файлами (если есть).
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            if not id:
                Content.objects.create(season=self.season,
                                       item=obj)
            return redirect('series_season_user',self.season.id)
        return self.render_to_response({'form':form,
                                        'object':self.obj})
    

class SeriesCinemaListView(ListView):
    model = Series
    template_name = 'series/series_home_page/list_series_home.html'
    context_object_name = 'series'

class SeriesDetailView(DetailView):
    model = Series
    template_name = 'series/series_home_page/detail_series.html'
    context_object_name = 'series'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seasons = self.object.season_series.all()
        context['seasons'] = [
            {
                'season': season,
                'contents': season.content_set.all()  
                # Получаем все контенты для каждого сезона
            }
            for season in seasons
        ]
        return context

#Предоставление просомтра юзером контента своих сериалов и редактитрования своего сериала
class SeasonVideoView(TemplateResponseMixin,View):
    template_name = 'series/series_home_page/season_video.html'

    def get(self,request,season_id):
        season = get_object_or_404(Season,
                                   id=season_id,
                                   series__user=request.user)
        return self.render_to_response({'season':season})
    

#Удаление видео с сайта. аккаунт модератора
class DeleteVideoSeriesView(View):
    def post(self,request,id):
        content = get_object_or_404(Content,
                                    id=id,
                                    season__series__user=request.user)
        season = content.season
        content.item.delete()
        content.delete()
        return redirect('series_season_user',season.id)  
    
