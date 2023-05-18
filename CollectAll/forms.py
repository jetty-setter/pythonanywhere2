from django import forms
from .models import Collection, CollectionType, CollectionItem, Category, Comment
from django.shortcuts import render



class CollectionCreate(forms.ModelForm):
    collection_type = forms.ChoiceField(choices=[('Collection', 'Collection'), ('Wishlist', 'Wishlist')], required=False)

    class Meta:
        model = Collection
        fields = ["name", "private", "favorite", "notes", "siteUser", "collection_image"]
        widgets = {'siteUser': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(CollectionCreate, self).__init__(*args, **kwargs)

        # Add choices to the collection_type field
        self.fields['collection_type'].choices = [('Collection', 'Collection'), ('Wishlist', 'Wishlist')]

    def clean(self):
        cleaned_data = super().clean()
        collection_type = cleaned_data.get('collection_type')

        if collection_type == '':
            raise forms.ValidationError("You must select a collection type.")

        return cleaned_data

    def save(self, commit=True):
        instance = super(CollectionCreate, self).save(commit=False)

        # Use the selected CollectionType
        collection_type = self.cleaned_data.get('collection_type')
        if collection_type == 'Collection':
            instance.collectionType = CollectionType.objects.get(name='Collection')
        elif collection_type == 'Wishlist':
            instance.collectionType = CollectionType.objects.get(name='Wishlist')

        if commit:
            instance.save()
        return instance


class CollectionItemCreate(forms.ModelForm):
    class Meta:
        model = CollectionItem
        fields = ["name", "quantity", "value", "notes", "collectedDate", "collectionItem_image", "collection"
                  ]
        widgets = {'collection': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(CollectionItemCreate, self).__init__(*args, **kwargs)

        # Add choices to the collection field
        existing_choices = [(c.id, c.name) for c in Collection.objects.all()]
        self.fields['collection'].choices = existing_choices

        # Get existing categories
        existing_categories = Category.objects.all()
#        category_choices = [(c.id, c.name) for c in existing_categories]

        # # If there are no existing categories, show the "New Category" field
        # if not existing_categories:
        #     self.fields['categories'] = forms.CharField(max_length=50, required=False, label='New Category')
        # # Otherwise, show the category dropdown
        # else:
        #     self.fields['categories'] = forms.ChoiceField(choices=[('', 'Select Category')] + category_choices,
        #                                                   label='Existing Categories', required=False)
        #     self.fields['new_category'] = forms.CharField(max_length=50, required=False, label='New Category')

    def clean(self):
        cleaned_data = super().clean()

        # If "New Category" field is not empty, use it as the category name
        new_category_name = cleaned_data.get('new_category')
        if new_category_name:
            cleaned_data['categories'] = Category.objects.create(name=new_category_name)
        return cleaned_data

    def save(self, commit=True):
        instance = super(CollectionItemCreate, self).save(commit=False)

        if commit:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comments']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CommentForm, self).__init__(*args, **kwargs)