from django.urls import path
from . import views

urlpatterns = [
    path('contact_app/', views.contact, name='contact_app'),
]
