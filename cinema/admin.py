from django.contrib import admin
from .models import *


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

@admin.register(Rating)
class RatingModelAdmin(admin.ModelAdmin):
    list_display = ['series','user','active']
    list_filter = ['user','created','updated',]
    search_fields = ['user','text']