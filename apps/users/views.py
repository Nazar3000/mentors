from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, ListView
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)

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


class SignOutView(LogoutView):
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        user_type = request.user.user_type
        auth_logout(request)
        next_page = self.get_next_page(user_type=user_type)
        if next_page:
            # Redirect to this page until the session has been cleared.
            return HttpResponseRedirect(next_page)
        return super().dispatch(request, *args, **kwargs)

    def get_next_page(self, user_type=None):
        if user_type == UserTypes.MENTOR:
            return resolve_url('users:signin')
        elif user_type == UserTypes.SOCIAL_SERVICE_CENTER:
            return resolve_url('social_services:ssc_login')
        elif user_type == UserTypes.PUBLIC_SERVICE:
            return resolve_url('public_services:po_login')
        elif user_type == UserTypes.GOVERN_USER:
            pass

        return super().get_next_page()


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
