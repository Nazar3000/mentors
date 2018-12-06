from django.urls import path, re_path
from . import views
from social_services.views import LoginView

app_name = 'public_services'

urlpatterns = [
    path('register/', views.PublicServiceSignUpFormView.as_view(), name='po_signup_step0'),
    path('login/', LoginView.as_view(), name='po_login'),
    path('main/', views.PublicServiceMainPageView.as_view(), name='main'),
    path('mentors/', views.PublicServiceMentorsView.as_view(), name='mentors'),
    path('mentors/<str:action>/', views.PublicServiceMentorsView.as_view(), name='mentors_post'),
    path('video/', views.PublicServiceVideoMentorView.as_view(), name='video'),
    path('dating/', views.PublicServiceDatingView.as_view(), name='dating'),
    path('material/', views.PublicServiceMaterialView.as_view(), name='material'),
    re_path(r'^mentors/mentor-card/(?P<pk>[\w-]+)/$', views.PublicServiceMentorCardView.as_view(), name='mentor_card'),
]
