from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a category name')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Comment(models.Model):
    collection = models.ForeignKey('Collection', on_delete=models.RESTRICT, null=True)
    siteUser = models.ForeignKey('SiteUser', on_delete=models.RESTRICT, null=True)
    comments = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.comments

class Collection(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a Collection Title')
    private = models.BooleanField()
    favorite = models.BooleanField()
    notes = models.TextField()
    collectionType = models.ForeignKey('CollectionType', on_delete=models.RESTRICT, null=True)
    siteUser = models.ForeignKey('SiteUser', on_delete=models.RESTRICT, null=True)
    parent = models.ForeignKey('Collection', on_delete=models.RESTRICT, null=True, blank=True)
    collection_image = models.ImageField(upload_to='images/', null=True, blank=True)
    categories = models.ManyToManyField('Category', related_name='collections', blank=True)
    comments = models.ManyToManyField('Comment', related_name='collection_comments', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('collection_detail', args=[str(self.id)])


class CollectionType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CollectionItem(models.Model):
    uniqueId = models.CharField(max_length=100, help_text='Enter a unique name for this item')
    name = models.CharField(max_length=200, help_text='Enter a name for this item')
    quantity = models.IntegerField()
    value = models.DecimalField(decimal_places=2, max_digits=100)
    notes = models.TextField()
    collectedDate = models.DateField()
    collection = models.ForeignKey('Collection', on_delete=models.RESTRICT, null=True)
    collectionItem_image = models.ImageField(upload_to='images/', null=True, blank=True)
#    categories = models.ManyToManyField('Category', related_name='items', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('collection_detail', args=[str(self.collection.id)])


class SiteUser(AbstractUser):
    private = models.BooleanField(null=True)
    first_name = models.CharField(max_length=150)
    description = models.TextField(null=True)
    user_image = models.ImageField(upload_to='images/', null=True, blank=True)
    favorite_collections = models.ManyToManyField(Collection, related_name='favored_by', blank=True)

    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])
