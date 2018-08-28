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
    path('', views.UnregisteredGuidelineView.as_view(), name='unregistered_guideline'),
    path('register/', views.SignUpStep0View.as_view(), name='signup_step0'),
    path('register-step1/', views.SignUpStep1View.as_view(), name='signup_step1'),
    path('register-step2/', views.SignUpStep2View.as_view(), name='signup_step2'),
    path('register-step3/', views.SignUpStep3View.as_view(), name='signup_step3'),
    path('roadmap/', views.MentorRoadmap.as_view(), name='mentor_roadmap')
]

