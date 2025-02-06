from django.contrib import admin
from .models import *


class SeasonInline(admin.StackedInline):
    model = Season


@admin.register(Series)
class ModelAdminSeries(admin.ModelAdmin):
    list_display = ['name','created','studio']
    list_filter = ['created','updated']
    prepopulated_fields = {'slug':('name',)}
    search_fields = ['name','description']
    inlines = [SeasonInline]


