from django.shortcuts import render
from social_services.views import SignUpFormView
from .forms import PublicOrganizationSignUpStep0Form
from django.views.generic import TemplateView
from .models import PublicServiceVideo


class PublicServiceSignUpFormView(SignUpFormView):
    form_class = PublicOrganizationSignUpStep0Form


class PublicServiceMainPageView(TemplateView):
    template_name = 'public_services/po_main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_video'] = PublicServiceVideo.objects.filter(page=1).first()
        return context


class PublicServiceVideoMentorView(TemplateView):
    template_name = 'public_services/po_video_mentor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentor_video'] = PublicServiceVideo.objects.filter(page=2).first()
        return context
