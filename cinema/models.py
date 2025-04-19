from django.db import models
from unidecode import unidecode
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from .fields import OrderField
from .models_crete_from_contenttype import *

class Series(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='series_creater')
    name = models.CharField(max_length=250,unique=True)
    cover = models.ImageField(upload_to='images/',blank=True)
    slug = models.SlugField(max_length=250,blank=True)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    studio = models.CharField(max_length=250)
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'Сериал'
        verbose_name_plural = 'Сериалы'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("series_detail", args=[self.id,
                                              self.slug,])
    

class Season(models.Model):
    series = models.ForeignKey(Series,
                               on_delete=models.CASCADE,
                               related_name='season_series')
    cover = models.ImageField(upload_to='images/',blank=True)
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    counter = OrderField(blank=True,for_fields=['series'])
    class Meta:
        ordering = ['created']
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'

    def __str__(self):
        return f"Сезон сериала {self.series.name} "
    

class Content(models.Model):
    season = models.ForeignKey(Season,
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in':(
                                         'video',
                                     )})
    counter = OrderField(blank=True,for_fields=['season'])
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type','object_id')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['created']


class ItemBase(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='%(class)s_related')
    title = models.CharField(max_length=250)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    comment = GenericRelation('Comment')
    class Meta:
        abstract = True

    def __str__(self):
        return self.title
    

class Video(ItemBase):
    video = models.FileField(upload_to='video/')

