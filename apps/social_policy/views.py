import os

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from xlsxwriter import Workbook

from mentors.models import MentorSocialServiceCenterData
from social_policy.models import ExtraRegionData, SPMaterial, SPMaterialCategory
from social_services.models import BaseSocialServiceCenter
from social_services.views import MentorsView, PairsView, PublicServicesView, MaterialView, PairDetailView
from users.constants import MentorStatuses, UserTypes
from users.models import Mentor, Coordinator, SocialServiceCenter, Organization, PublicService
from .forms import SPAuthenticationForm


class CheckIfUserIsSocialPolicyMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.user_type == UserTypes.SOCIAL_POLICY_MINISTRY
        return False


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


class MainPageView(CheckIfUserIsSocialPolicyMixin, TemplateView):
    template_name = 'social_policy/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)

        context['organization_count'] = Organization.objects.count()
        context['social_service_center_count'] = BaseSocialServiceCenter.objects.count()
        context['public_service_count'] = PublicService.objects.filter(contract_number__isnull=False).count()

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

    @staticmethod
    def get_social_service_stats(district_data, service):
        district_data['public_service_count'] += service.publicservice_set.count()

        related_coordinators = Coordinator.objects.filter(
            (Q(social_service_center=service)
             | Q(public_service__in=service.publicservice_set.all())
             & Q(mentors__isnull=False)
             & Q(mentors__mentoree__isnull=False)
             )
        )
        district_data['child_count'] += related_coordinators.count()

        related_mentors = Mentor.objects.filter(coordinator__in=related_coordinators)
        district_data['organization_count'] += related_mentors\
            .exclude(mentoree__organization__isnull=True).count()
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

    def get_district_data(self, request):
        if request.GET['district_id'] == 'Київська':
            q_region = Q(region=request.GET['district_id']) | Q(region='Київ')
        else:
            q_region = Q(region=request.GET['district_id'])

        base_centers = BaseSocialServiceCenter.objects.filter(q_region)

        services_related = base_centers.select_related('service').prefetch_related('service__publicservice_set')

        district_data = {
            'district_name': '{} область'.format(request.GET['district_id']),
            'children_in_organizations_count': ExtraRegionData.objects.get(q_region).child_count,
            'organization_count': 0,
            'social_service_center_count': 0,
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
                district_data['social_service_center_count'] += 1
                district_data = self.get_social_service_stats(district_data, base_service.service)

        return district_data

    def get(self, request, *args, **kwargs):
        if 'district_id' in request.GET.keys() and 'search_value' not in request.GET.keys():
            return JsonResponse(self.get_district_data(request))
        elif 'search_value' in request.GET.keys():
            if request.GET['district_id'] == 'Київська':
                q_region = Q(basesocialservicecenter__region=request.GET['district_id']) \
                           | Q(basesocialservicecenter__region='Київ')
            else:
                q_region = Q(basesocialservicecenter__region=request.GET['district_id'])

            filtered_base_soc_centers = SocialServiceCenter.objects.filter(
                (Q(city__icontains=request.GET['search_value'])
                 | Q(name__icontains=request.GET['search_value'])
                 | Q(address__icontains=request.GET['search_value']))
                & q_region).values(
                'pk',
                'name',
            )
            return JsonResponse(list(filtered_base_soc_centers), safe=False)
        elif 'social_service_id' in request.GET.keys():
            service_data = {
                'public_service_count': 0,
                'child_count': 0,
                'licenced_mentor_count': 0,
                'psychologist_mentor_count': 0,
                'infomeeting_mentor_count': 0,
                'applied_questionnaire_count': 0,
                'pairs_disbanded_count': 0,
            }
            service_data = self.get_social_service_stats(
                service_data, SocialServiceCenter.objects.get(pk=request.GET['social_service_id']))
            return JsonResponse(service_data)
        elif 'regions_table' in request.GET.keys():
            regions_data = list(ExtraRegionData.objects.all().values('region', 'child_count'))
            for region in regions_data:
                if region['region'] == 'Київська':
                    q_region = Q(region=region['region']) | Q(region='Київ')
                else:
                    q_region = Q(region=region['region'])

                related_base_services = BaseSocialServiceCenter.objects.filter(q_region).select_related('service')
                mentoree_count = 0
                admitted_to_child_count = 0
                passed_training_count = 0
                for base_service in related_base_services:
                    if base_service.service:
                        related_coordinators = Coordinator.objects.filter(
                            (Q(social_service_center=base_service.service)
                             | Q(public_service__in=base_service.service.publicservice_set.all())
                             & Q(mentors__isnull=False)
                             & Q(mentors__mentoree__isnull=False)
                             )
                        )
                        related_mentors = Mentor.objects.filter(coordinator__in=related_coordinators)

                        mentoree_count += related_mentors.filter(meetings__isnull=False).count()
                        admitted_to_child_count += related_mentors\
                            .filter(social_service_center_data__admitted_to_child=True).count()
                        passed_training_count += related_mentors\
                            .filter(social_service_center_data__training_date__isnull=False).count()

                region['mentoree_count'] = mentoree_count
                region['admitted_to_child_count'] = admitted_to_child_count
                region['passed_training_count'] = passed_training_count

            if 'xlsx' in request.GET.keys():
                ordered_list = ['region', 'child_count', 'mentoree_count',
                                'admitted_to_child_count', 'passed_training_count']
                header_list = ['Область', 'Дітей в закладах', 'Дітей з наставниками',
                               'Наставників з висновками (за весь час)',
                               'Наставників, які пройшли курс підготовки (за весь час)']
                filename = 'зведена таблиця.xlsx'

                return self.get_xlsx_response(filename, ordered_list, header_list, regions_data)

            return JsonResponse(regions_data, safe=False)

        return super().get(request, *args, **kwargs)

    @staticmethod
    def get_xlsx_response(filename, ordered_list, header_list, data):
        wb = Workbook(filename)
        ws = wb.add_worksheet()

        first_row = 0
        for header in header_list:
            col = header_list.index(header)  # we are keeping order.
            ws.write(first_row, col, header)  # we have written first row which is the header of worksheet also.

        row = 1
        for data_dict in data:
            for _key, _value in data_dict.items():
                col = ordered_list.index(_key)
                ws.write(row, col, _value)
            row += 1  # enter the next row
        wb.close()
        with open(filename, 'rb') as f:
            data = f.read()

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
            response.write(data)
        os.remove(filename)

        return response


class SPMentorsView(CheckIfUserIsSocialPolicyMixin, MentorsView):
    template_name = 'social_policy/mentors.html'

    def get_public_service(self):
        return PublicService.objects.all()

    def get_mentors_query_data(self, fields_select_query):
        mentors_query_data = Mentor.objects.raw("""
            SELECT
                users_mentor.user_id,
                {fields_select_query}
            FROM users_mentor
                JOIN users_coordinator ON users_mentor.coordinator_id = users_coordinator.id
                JOIN mentors_mentorlicencekey ON users_mentor.licence_key_id = mentors_mentorlicencekey.id
        """.format(fields_select_query=fields_select_query))
        return mentors_query_data


class SPPairsView(CheckIfUserIsSocialPolicyMixin, PairsView):
    template_name = 'social_policy/pairs.html'

    def get_public_service(self):
        return PublicService.objects.all()

    def get_mentors_query_data(self, fields_select_query):
        mentors_query_data = Mentor.objects.raw("""
            SELECT
                users_mentor.user_id,
                {fields_select_query}
            FROM users_mentor
                JOIN users_coordinator ON users_mentor.coordinator_id = users_coordinator.id
                JOIN mentors_mentorlicencekey ON users_mentor.licence_key_id = mentors_mentorlicencekey.id
        """.format(fields_select_query=fields_select_query))
        return mentors_query_data


class SPPairDetailView(CheckIfUserIsSocialPolicyMixin, PairDetailView):
    template_name = 'social_policy/pair_detail.html'


class SPPublicServicesView(CheckIfUserIsSocialPolicyMixin, PublicServicesView):
    template_name = 'social_policy/public_services.html'

    def filter_public_service(self):
        return PublicService.objects.all()


class SPMaterialView(CheckIfUserIsSocialPolicyMixin, MaterialView):
    model = SPMaterial
    template_name = 'social_policy/material.html'

    def get_context_data(self, **kwargs):
        context = super(MaterialView, self).get_context_data(**kwargs)
        context['object_list'] = context['object_list'].order_by('id')
        context['categories'] = SPMaterialCategory.objects.all()
        return context
