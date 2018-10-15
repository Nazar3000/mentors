from django.shortcuts import render
from social_services.views import SignUpFormView
from .forms import PublicOrganizationSignUpStep0Form


class PublicOrganizationSignUpFormView(SignUpFormView):
    form_class = PublicOrganizationSignUpStep0Form
