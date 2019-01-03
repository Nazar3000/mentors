from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib import messages

from mentors.models import MentorSocialServiceCenterData
from social_services.models import SocialServiceVideo
from users.models import Mentor
from .forms import SPAuthenticationForm


class SPLoginView(FormView):
    template_name = 'social_policy/login.html'
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
        return redirect('social_policy:main')


class MainPageView(TemplateView):
    template_name = 'social_policy/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)

        context['licenced'] = Mentor.objects.filter(licenced=True).count()
        context['psychologist_met'] = MentorSocialServiceCenterData.objects\
            .filter(psychologist_meeting_date__isnull=False).count()
        context['infomeeting_made'] = MentorSocialServiceCenterData.objects\
            .filter(infomeeting_date__isnull=False).count()
        context['training_made'] = MentorSocialServiceCenterData.objects\
            .filter(training_date__isnull=False).count()
        context['admitted_to_child'] = MentorSocialServiceCenterData.objects\
            .filter(admitted_to_child=True).count()
        context['contract_subscribed'] = MentorSocialServiceCenterData.objects\
            .filter(contract_number__isnull=False).count()

        context['total'] = MentorSocialServiceCenterData.objects.all().count()

        def get_percentage(value):
            return int(round((value / context['total']) * 100))

        if context['total'] > 0:
            context['licenced_percentage'] = get_percentage(context['licenced'])
            context['psychologist_percentage'] = get_percentage(context['psychologist_met'])
            context['infomeeting_percentage'] = get_percentage(context['infomeeting_made'])
            context['training_percentage'] = get_percentage(context['training_made'])
            context['admitted_to_child_percentage'] = get_percentage(context['admitted_to_child'])
            context['contract_subscribed_percentage'] = get_percentage(context['contract_subscribed'])
        else:
            context['licenced_percentage'] = 0
            context['psychologist_percentage'] = 0
            context['infomeeting_percentage'] = 0
            context['training_percentage'] = 0
            context['admitted_to_child_percentage'] = 0
            context['contract_subscribed_percentage'] = 0
        return context
