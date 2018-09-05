from django.contrib.auth.views import LoginView
from django.shortcuts import resolve_url
from django.views import View
from django.views.generic import TemplateView

from .constants import UserTypes


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
            pass
        elif user_type == UserTypes.PUBLIC_SERVICE:
            pass
        elif user_type == UserTypes.GOVERN_USER:
            pass
