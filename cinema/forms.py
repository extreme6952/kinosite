from .models import *
from django import forms
from django.forms.models import inlineformset_factory

formset_season = inlineformset_factory(Series,
                                Season,
                                fields=['title','description'],
                                extra=2)