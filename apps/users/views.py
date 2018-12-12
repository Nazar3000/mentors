from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url
from django.views.generic import TemplateView, ListView

from users.models import Material, MaterialCategory
from .constants import UserTypes, MaterialTypes


class UnregisteredGuidelineView(TemplateView):
    template_name = 'users/guideline.html'


class SignInView(LoginView):
    template_name = 'users/signin.html'

    def get_success_url(self):
        user_type = self.request.user.user_type
        # TODO: Complete another user types redirect
        if user_type == UserTypes.MENTOR:
            return resolve_url('mentors:mentor_office')
        elif user_type == UserTypes.SOCIAL_SERVICE_CENTER:
            return resolve_url('social_services:main')
        elif user_type == UserTypes.PUBLIC_SERVICE:
            return resolve_url('public_services:main')
        elif user_type == UserTypes.GOVERN_USER:
            pass

        return resolve_url('users:unregistered_guideline')


class OrganizationMaterialView(ListView):
    model = Material
    template_name = 'users/material.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = context['object_list'] \
            .filter(material_type=MaterialTypes.ORGANIZATION.name).order_by('id')
        context['categories'] = MaterialCategory.objects.filter()
        return context


class SSDMaterialView(OrganizationMaterialView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = context['object_list'] \
            .filter(material_type=MaterialTypes.SSD.name).order_by('id')
        context['categories'] = MaterialCategory.objects.filter()
        return context
