from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [
    path('login/',
         views.SignInView.as_view(),
         name='signin'),
    path('logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),
    path('', views.UnregisteredGuidelineView.as_view(), name='unregistered_guideline')
]
