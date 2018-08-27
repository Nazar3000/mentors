from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


app_name = 'users'

urlpatterns = [
    path('signin/',
         views.SignInView.as_view(),
         {'template_name': 'users/login.html'},
         name='signin'),
    path('logout/',
         auth_views.LogoutView.as_view(),
         {'next_page': 'login'},
         name='logout'),
    path('signup/', views.SignUpView.as_view(), name='signup')
]
