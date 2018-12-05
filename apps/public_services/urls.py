from django.urls import path
from . import views
from social_services.views import LoginView

app_name = 'public_services'

urlpatterns = [
    path('register/', views.PublicServiceSignUpFormView.as_view(), name='po_signup_step0'),
    path('login/', LoginView.as_view(), name='po_login'),
    path('main/', views.PublicServiceMainPageView.as_view(), name='main'),
    path('video/', views.PublicServiceVideoMentorView.as_view(), name='video'),
]
