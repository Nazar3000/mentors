from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView

from .models import Mentor
from .forms import SignUpStep0Form, SignUpStep1Form


class SignInView(LoginView):
    template_name = 'users/signin.html'


class SignUpStep0View(FormView):
    template_name = 'users/signup_step0.html'
    form_class = SignUpStep0Form
    success_url = reverse_lazy('users:signup_step1')

    def form_valid(self, form):
        self.request.session['mentor_data'] = form.cleaned_data
        return HttpResponseRedirect(self.get_success_url())


class SignUpStep1View(CreateView):
    template_name = 'users/signup_step1.html'
    form_class = SignUpStep1Form
    success_url = reverse_lazy('users:signup_step2')

    def form_valid(self, form):
        user = form.save()
        if 'mentor_data' in self.request.session.keys():
            mentor = Mentor(**self.request.session['mentor_data'])
            mentor.user = user
            mentor.save()
        else:
            return redirect('users:signup_step0')
        return HttpResponseRedirect(self.get_success_url())


class SignUpStep2View(TemplateView):
    template_name = 'users/signup_step2.html'


class UnregisteredGuidelineView(TemplateView):
    template_name = 'users/guideline.html'
