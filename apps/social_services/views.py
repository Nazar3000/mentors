import datetime
import json

from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils import formats
from django.views.generic import TemplateView

from mentors.models import MentorSocialServiceCenterData, MentorLicenceKey
from social_services.forms import MentorEditForm
from users.constants import MentorStatuses
from users.models import Mentor, PublicService, Coordinator, SocialServiceCenter
from users.templatetags.date_tags import get_age


class MentorsView(TemplateView):
    template_name = 'social_services/mentors.html'

    @staticmethod
    def get_responsible_pk(mentor):
        try:
            responsible = mentor.coordinator.social_service_center.pk
        except SocialServiceCenter.DoesNotExist:
            responsible = mentor.coordinator.public_service.pk
        except (Coordinator.DoesNotExist, PublicService.DoesNotExist):
            responsible = None
        return responsible

    def get_light_data(self):
        mentor_statuses = dict(MentorStatuses.choices())
        related_public_services = PublicService.objects.filter(
            social_service_center__pk=self.request.user.pk).values('pk', 'name')
        mentors_data = Mentor.objects.all().values(
            'pk',
            'questionnaire__full_name',
            'phone_number',
            'licence_key__key',
            'status',
        )
        for data in mentors_data:
            mentor = Mentor.objects.get(pk=data['pk'])
            soc_service_data, created = MentorSocialServiceCenterData.objects.get_or_create(mentor=mentor)
            data['docs_status'] = soc_service_data.docs_status
            data['responsible'] = self.get_responsible_pk(mentor)

        return JsonResponse({
            'mentors_data': list(mentors_data),
            'mentor_statuses': mentor_statuses,
            'public_services': list(related_public_services)
        })

    def get_extended_data(self):
        mentor = Coordinator.objects.get(social_service_center__pk=self.request.GET['soc_service_id']).mentor
        mentor_data = model_to_dict(mentor, fields=(
            'first_name',
            'last_name',
            'status',
            'phone_number',
        ))
        mentor_data['pk'] = mentor.pk
        mentor_data['email'] = mentor.user.email
        mentor_data['licence_key'] = mentor.licence_key.key
        mentor_data['date_of_birth'] = mentor.questionnaire.date_of_birth.strftime('%d.%m.%Y')
        mentor_data['age'] = get_age(mentor.questionnaire.date_of_birth)
        mentor_data['address'] = mentor.questionnaire.actual_address
        mentor_data['questionnaire_creation_date'] = formats.date_format(mentor.questionnaire.creation_date)
        mentor_data['responsible'] = self.get_responsible_pk(mentor)
        mentor_data['profile_image'] = mentor.profile_image.url if mentor.profile_image else ''

        mentor_social_service_center_data = model_to_dict(mentor.social_service_center_data)
        if mentor.social_service_center_data.infomeeting_date:
            mentor_social_service_center_data['infomeeting_date'] = formats.date_format(
                mentor.social_service_center_data.infomeeting_date)
        if mentor.social_service_center_data.psychologist_meeting_date:
            mentor_social_service_center_data['psychologist_meeting_date'] = formats.date_format(
                mentor.social_service_center_data.psychologist_meeting_date)
        if mentor.social_service_center_data.training_date:
            mentor_social_service_center_data['training_date'] = formats.date_format(
                mentor.social_service_center_data.training_date)
        if mentor.social_service_center_data.contract_date:
            mentor_social_service_center_data['contract_date'] = formats.date_format(
                mentor.social_service_center_data.contract_date)
        print(mentor_social_service_center_data)

        if mentor.mentoree:
            mentor_social_service_center_data['mentoree_name'] = '{} {}'.format(
                mentor.mentoree.first_name, mentor.mentoree.last_name)
        else:
            mentor_social_service_center_data['mentoree_name'] = ''
        return JsonResponse({'mentor_data': mentor_data,
                             'mentor_social_service_center_data': mentor_social_service_center_data})

    def get(self, request, *args, **kwargs):
        if 'get_light_data' in request.GET.keys():
            return self.get_light_data()

        elif 'get_extended_data' in request.GET.keys():
            return self.get_extended_data()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if 'change_light_data' in data.keys():
            light_data = data['change_light_data']
            for d in light_data:
                mentor = Mentor.objects.get(pk=d['pk'])
                mentor.status = d['status']
                coordinator = Coordinator.get_coordinator_by_related_service_pk(d['responsible'])
                coordinator.mentor = mentor
                coordinator.save()
                mentor.save()
        elif 'change_extended_data' in data.keys():
            extended_data = data['change_extended_data']
            licence_key = extended_data.pop('licence_key')
            form = MentorEditForm(extended_data, instance=Mentor.objects.get(pk=extended_data['pk']))
            if form.is_valid():
                mentor = form.save(commit=False)
                if mentor.licence_key:
                    mentor.licence_key.key = licence_key
                    mentor.licence_key.save()
                else:
                    key = MentorLicenceKey.objects.create(key=licence_key)
                    mentor.licence_key = key
                mentor.save()
            else:
                return JsonResponse(dict(form.errors.items()))

        return JsonResponse({'status': 'success'})
