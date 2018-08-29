from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView


class UnregisteredGuidelineView(TemplateView):
    template_name = 'users/guideline.html'


class SignInView(LoginView):
    template_name = 'users/signin.html'
