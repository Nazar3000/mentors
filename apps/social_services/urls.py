from django.urls import path

from . import views

app_name = 'social_services'

urlpatterns = [
    path('mentors/', views.MentorsView.as_view(), name='mentors'),
]
