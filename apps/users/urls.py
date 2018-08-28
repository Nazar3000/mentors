from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [
    path('login/',
         views.SignInView.as_view(),
         {'template_name': 'users/login.html'},
         name='signin'),
    path('logout/',
         auth_views.LogoutView.as_view(),
         {'next_page': 'login'},
         name='logout'),
    path('register/', views.SignUpStep1View.as_view(), name='signup_step1'),
    path('', views.UnregisteredGuidelineView.as_view(), name='unregistered_guideline')
]
