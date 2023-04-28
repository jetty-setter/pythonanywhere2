from django import forms
from django.contrib.auth.forms import UserCreationForm
from CollectAll.models import SiteUser

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, help_text='Required.')
    last_name = forms.CharField(max_length=30, help_text='Required.')
    class Meta:
        model = SiteUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = SiteUser

