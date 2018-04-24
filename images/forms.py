from django import forms
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
    choices=[(obj.id, obj.name) for obj in Album.objects.all()]
    album = forms.ChoiceField(choices=choices)


class ExtendedImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'description', 'pic']

       
