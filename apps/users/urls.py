from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('login/',
         views.SignInView.as_view(),
         name='signin'),
    path('logout/',
         views.SignOutView.as_view(),
         name='logout'),
    path('', views.UnregisteredGuidelineView.as_view(), name='unregistered_guideline'),
    path('organization-material/', views.OrganizationMaterialView.as_view(), name='organization_material'),
    path('ssd-material/', views.SSDMaterialView.as_view(), name='ssd_material'),
]
