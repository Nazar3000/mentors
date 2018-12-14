from django.urls import path, re_path
from . import views

app_name = 'public_services'

urlpatterns = [
    path('register/', views.PublicServiceSignUpFormView.as_view(), name='po_signup_step0'),
    path('login/', views.PublicServiceLoginView.as_view(), name='po_login'),
    path('main/', views.PublicServiceMainPageView.as_view(), name='main'),
    path('mentors/', views.PublicServiceMentorsView.as_view(), name='mentors'),
    path('mentors/<str:action>/', views.PublicServiceMentorsView.as_view(), name='mentors_post'),
    path('video/', views.PublicServiceVideoMentorView.as_view(), name='video'),
    path('dating/', views.PublicServiceDatingView.as_view(), name='dating'),
    path('material/', views.PublicServiceMaterialView.as_view(), name='material'),
    path('question/', views.QuestionView.as_view(), name='question'),
    re_path(r'^mentors/mentor-card/(?P<pk>[\w-]+)/$', views.PublicServiceMentorCardView.as_view(), name='mentor_card'),
]
