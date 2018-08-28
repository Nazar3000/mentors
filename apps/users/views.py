from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import SignUpStep1Form, SignUpForm


class SignInView(LoginView):
    template_name = 'users/signin.html'


class SignUpStep1View(CreateView):
    template_name = 'users/signup_step1.html'
    form_class = SignUpStep1Form
    success_url = '/'  # TODO: specify correct success_url


class SignUpView(CreateView):
    template_name = 'users/signup_step0.html'
    form_class = SignUpForm
    success_url = '/'  # TODO: specify correct success_url


class UnregisteredGuidelineView(TemplateView):
    template_name = 'users/guideline.html'
