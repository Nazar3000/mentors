from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib import messages

from mentors.models import MentorSocialServiceCenterData
from social_services.models import SocialServiceVideo, BaseSocialServiceCenter
from users.constants import MentorStatuses
from users.models import Mentor, Coordinator
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

    def get_district_data(self, request):
        if request.GET['district_id'] == 'Київська':
            base_centers = BaseSocialServiceCenter \
                .objects.filter(Q(region=request.GET['district_id']) | Q(region='Київ'))
        else:
            base_centers = BaseSocialServiceCenter.objects.filter(region=request.GET['district_id'])

        services_related = base_centers.select_related('service').prefetch_related('service__publicservice_set')

        district_data = {
            'district_name': '{} область'.format(request.GET['district_id']),
            'public_service_count': 0,
            'child_count': 0,
            'licenced_mentor_count': 0,
            'psychologist_mentor_count': 0,
            'infomeeting_mentor_count': 0,
            'applied_questionnaire_count': 0,
            'pairs_disbanded_count': 0,
        }

        for base_service in services_related:
            if base_service.service:
                district_data['public_service_count'] += base_service.service.publicservice_set.count()

                related_coordinators = Coordinator.objects.filter(
                    (Q(social_service_center=base_service.service)
                     | Q(public_service__in=base_service.service.publicservice_set.all())
                     & Q(mentors__isnull=False)
                     & Q(mentors__mentoree__isnull=False)
                     )
                )
                district_data['child_count'] += related_coordinators.count()

                related_mentors = Mentor.objects.filter(coordinator__in=related_coordinators)
                district_data['licenced_mentor_count'] += related_mentors.filter(licenced=True).count()
                district_data['psychologist_mentor_count'] += related_mentors \
                    .exclude(social_service_center_data__psychologist_meeting_date__isnull=True).count()
                district_data['infomeeting_mentor_count'] += related_mentors \
                    .exclude(social_service_center_data__infomeeting_date__isnull=True).count()
                district_data['applied_questionnaire_count'] += related_mentors \
                    .exclude(questionnaire__isnull=True).count()
                district_data['pairs_disbanded_count'] += related_mentors \
                    .filter(status=MentorStatuses.PAIR_DISBANDED.name).count()
        return district_data

    def get(self, request, *args, **kwargs):
        if 'district_id' in request.GET.keys():
            return JsonResponse(self.get_district_data(request))

        return super().get(request, *args, **kwargs)
