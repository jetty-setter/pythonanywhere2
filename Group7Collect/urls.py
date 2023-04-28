from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('CollectAll.urls')),
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('register.urls')),
]
