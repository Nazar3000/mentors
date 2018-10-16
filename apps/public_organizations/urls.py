from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from . import views
from social_services.views import LoginView

app_name = 'public_organizations'

urlpatterns = [
    path('register/', views.PublicOrganizationSignUpFormView.as_view(), name='po_signup_step0'),
    path('login/', LoginView.as_view(), name='po_login'),
    path('main/', views.PublicOrganizationMainPageView.as_view(), name='main'),
    path('video/', views.PublicOrganizationVideoMentorView.as_view(), name='video'),
]
