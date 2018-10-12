from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from . import views

app_name = 'social_service'

urlpatterns = [
    path('register/', views.SignUpFormView.as_view(), name='ssc_signup_step0'),
    path('login/', views.LoginView.as_view(), name='ssc_login'),
    path('main/', views.MainPageView.as_view(), name='main'),
    path('video/', views.VideoMentorView.as_view(), name='video'),
    re_path(r'^mentor_card/(?P<pk>[\w-]+)/$', views.MentorCardView.as_view(), name='mentor_card'),
    path('material/', views.MaterialView.as_view(), name='material'),
    path('download_file/<int:material_id>/', views.download_file, name='download_file'),
]
