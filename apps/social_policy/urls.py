from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from . import views


app_name = 'social_policy'

urlpatterns = [
    path('login/', views.SPLoginView.as_view(), name='sp_login'),
    path('main/', views.MainPageView.as_view(), name='main'),
]