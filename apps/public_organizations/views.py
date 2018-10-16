from django.shortcuts import render
from social_services.views import SignUpFormView
from .forms import PublicOrganizationSignUpStep0Form
from django.views.generic import TemplateView
from .models import PublicOrganizationVideo


class PublicOrganizationSignUpFormView(SignUpFormView):
    form_class = PublicOrganizationSignUpStep0Form


class PublicOrganizationMainPageView(TemplateView):
    template_name = 'public_organizations/po_main.html'

    def get_context_data(self, **kwargs):
        context = super(PublicOrganizationMainPageView, self).get_context_data(**kwargs)
        context['main_video'] = PublicOrganizationVideo.objects.filter(page=1).first()
        return context


class PublicOrganizationVideoMentorView(TemplateView):
    template_name = 'public_organizations/po_video_mentor.html'

    def get_context_data(self, **kwargs):
        context = super(PublicOrganizationVideoMentorView, self).get_context_data(**kwargs)
        context['mentor_video'] = PublicOrganizationVideo.objects.filter(page=2).first()
        return context
