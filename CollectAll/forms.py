from django.forms import ModelForm
from django import forms
from .models import Collection


class CollectionCreate(ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "private", "favorite", "notes", "collectionType", "siteUser",'collection_image']
        widgets = {'siteUser': forms.HiddenInput()}
