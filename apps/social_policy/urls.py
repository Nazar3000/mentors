from django.urls import path
from . import views


app_name = 'social_policy'

urlpatterns = [
    path('login/', views.SPLoginView.as_view(), name='sp_login'),
    path('main/', views.MainPageView.as_view(), name='main'),
    path('mentors/', views.SPMentorsView.as_view(), name='mentors'),
    path('mentors/<str:action>/', views.SPMentorsView.as_view(), name='mentors_post'),
    path('pairs/', views.SPPairsView.as_view(), name='pairs'),
    path('public-services/', views.SPPublicServicesView.as_view(), name='public_services'),
    path('public-services/<str:action>/', views.SPPublicServicesView.as_view(), name='public_services_post'),
    path('material/', views.SPMaterialView.as_view(), name='material'),
]
