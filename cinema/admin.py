from django.contrib import admin
from .models import *
from .models_crete_from_contenttype import Comment

class SeasonInline(admin.StackedInline):
    model = Season

@admin.register(Series)
class ModelAdminSeries(admin.ModelAdmin):
    list_display = ['name','created','studio',]
    list_filter = ['created','updated']
    prepopulated_fields = {'slug':('name',)}
    search_fields = ['name','description']
    inlines = [SeasonInline]

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created']
    list_filter = ['counter']
    ordering = ['created']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created']
    search_fields = ['title']

# Регистрация связанной модели через GenericForeignKey
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['season', 'item', 'created','counter']
    list_filter = ['season', 'content_type']
     # Для удобного выбора связанных объектов

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['user','content_type','created']
    list_filter = ['created','updated','content_type']
    search_fields = ['user','text',]