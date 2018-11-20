from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'social_services'

urlpatterns = [
    path('register/', views.SignUpFormView.as_view(), name='ssc_signup_step0'),
    path('login/', views.LoginView.as_view(), name='ssc_login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('main/', views.MainPageView.as_view(), name='main'),
    path('video/', views.VideoMentorView.as_view(), name='video'),
    re_path(r'^mentor-card/(?P<pk>[\w-]+)/$', views.MentorCardView.as_view(), name='mentor_card'),
    path('material/', views.MaterialView.as_view(), name='material'),
    path('download_file/<int:material_id>/', views.download_file, name='download_file'),
    path('mentors/', views.MentorsView.as_view(), name='mentors'),
    path('mentors/<str:action>/', views.MentorsView.as_view(), name='mentors_post'),
    path('public-services/', views.PublicServicesView.as_view(), name='public_services'),
    path('public-services/<str:action>/', views.PublicServicesView.as_view(), name='public_services_post'),
    path('dating/', views.DatingView.as_view(), name='dating'),
    path('pair/<uuid:pk>/', views.PairDetailView.as_view(), name='pair_detail'),
]
