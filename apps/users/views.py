from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from .forms import SignUpForm


class SignInView(LoginView):
    template_name = 'users/signin.html'


class SignUpView(CreateView):
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = '/'  # TODO: specify correct success_url
