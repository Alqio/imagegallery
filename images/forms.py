from django import forms
from django.db import OperationalError, ProgrammingError

from images.models import Album, Image
from django.forms import ModelForm, Textarea, TextInput, NumberInput


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'description']

        widgets = {
            'description': Textarea(attrs={
                'cols': 40,
                'rows': 4,
                'class': 'form-control'
            })
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'description', 'pic']
        widgets = {
            'description': Textarea(attrs={
                'cols': 40,
                'rows': 4,
                'class': 'form-control'
            })
        }

    # This try except is required for makemigrations as Album relation might not exist yet
    try:
        choices = [(obj.id, obj.name) for obj in Album.objects.all()]
    except (OperationalError, ProgrammingError) as e:
        choices = []

    for choice in choices:
        print(choice)
    album = forms.ChoiceField(choices=choices)


class ExtendedImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'description', 'pic']


