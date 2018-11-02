from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SPAuthenticationForm


class SPLoginView(FormView):
    template_name = 'social_policy/sp_login.html'
    form_class = SPAuthenticationForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
        else:
            messages.error(self.request, 'Невірний пароль.')
            return redirect('social_policy:sp_login')
        return redirect('/')


class MainPageView(TemplateView):
    template_name = 'social_policy/sp_social.html'
