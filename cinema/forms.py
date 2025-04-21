from .models import *
from django import forms
from django.forms.models import inlineformset_factory

class AddSeasonForm(forms.Form):
    season = forms.ModelChoiceField(queryset=Season.objects.all(),
                                    widget=forms.HiddenInput) 

class AddSeriesUser(forms.ModelForm):
    class Meta:
        model = Series
        fields = ['name','cover','description','studio' ]

    def __init__(self,*args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'placeholder':'Название',
        })
        self.fields['cover'].widget.attrs.update({
            'placeholder':'Обложка сериала',
        })
        self.fields['description'].widget.attrs.update({
            'placeholder':'Описание',
        })
        self.fields['studio'].widget.attrs.update({
            'placeholder':'Студия',
        })