from django.urls import path

from . import views

app_name = 'volunteers'

urlpatterns = [
    path('became-a-volunteer/', views.VolunteerSignUpView.as_view(), name='volunteer_signup')
]
