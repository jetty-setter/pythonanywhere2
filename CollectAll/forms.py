from django import forms
from .models import Collection, CollectionType, CollectionItem, Category

class CollectionCreate(forms.ModelForm):
    collection_type = forms.ChoiceField(choices=[], required=False)
    new_collection_type = forms.CharField(required=False)

    class Meta:
        model = Collection
        fields = ["name", "private", "favorite", "notes", "siteUser", "collection_image"]
        widgets = {'siteUser': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(CollectionCreate, self).__init__(*args, **kwargs)

        # Add choices to the collection_type field
        existing_choices = [(ct.id, ct.name) for ct in CollectionType.objects.all()]
        self.fields['collection_type'].choices = [('', 'Choose existing collection type')] + existing_choices + [
            ('new', 'Or create new collection type')]

    def clean(self):
        cleaned_data = super().clean()
        collection_type = cleaned_data.get('collection_type')
        new_collection_type = cleaned_data.get('new_collection_type')

        if collection_type == '' and not new_collection_type:
            raise forms.ValidationError("You must select an existing collection type or create a new one.")

        if collection_type != '' and new_collection_type:
            raise forms.ValidationError(
                "You cannot select an existing collection type and create a new one at the same time, your collection "
                "can only have one collection type assigned to it.")

        return cleaned_data

    def save(self, commit=True):
        instance = super(CollectionCreate, self).save(commit=False)

        # Check if a new collection type was specified
        new_collection_type_name = self.cleaned_data.get('new_collection_type')
        if new_collection_type_name:
            # Check if a CollectionType with this name already exists
            collection_type, created = CollectionType.objects.get_or_create(name=new_collection_type_name)
            instance.collectionType = collection_type
        else:
            # Use the selected CollectionType
            collection_type_id = self.cleaned_data.get('collection_type')
            if collection_type_id != '':  # Check if an existing CollectionType was selected
                instance.collectionType = CollectionType.objects.get(id=collection_type_id)
            else:
                instance.collectionType = None

        if commit:
            instance.save()
        return instance


class CollectionItemCreate(forms.ModelForm):
    class Meta:
        model = CollectionItem
        fields = ["name", "quantity", "value", "notes", "collectedDate", "collectionItem_image", "collection", "categories"]
        widgets = {'collection': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(CollectionItemCreate, self).__init__(*args, **kwargs)

        # Add choices to the collection field
        existing_choices = [(c.id, c.name) for c in Collection.objects.all()]
        self.fields['collection'].choices = existing_choices

        # Get existing categories
        existing_categories = Category.objects.all()
        category_choices = [(c.id, c.name) for c in existing_categories]

        # If there are no existing categories, show the "New Category" field
        if not existing_categories:
            self.fields['categories'] = forms.CharField(max_length=50, required=False, label='New Category')
        # Otherwise, show the category dropdown
        else:
            self.fields['categories'] = forms.ChoiceField(choices=[('', 'Select Category')] + category_choices, label='Existing Categories', required=False)
            self.fields['new_category'] = forms.CharField(max_length=50, required=False, label='New Category')

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
