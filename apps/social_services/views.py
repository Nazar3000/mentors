import datetime

from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils import formats
from django.views.generic import TemplateView

from users.constants import MentorStatuses
from users.models import Mentor, PublicService, Coordinator
from users.templatetags.date_tags import get_age


class MentorsView(TemplateView):
    template_name = 'social_services/mentors.html'

    def get(self, request, *args, **kwargs):
        if 'get_light_data' in request.GET.keys():
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
                data['docs_status'] = Mentor.objects.get(pk=data['pk']).docs_status
            return JsonResponse({
                'mentors_data': list(mentors_data),
                'mentor_statuses': mentor_statuses,
                'public_services': list(related_public_services)
            })
        elif 'get_extended_data' in request.GET.keys():
            mentor = Coordinator.objects.get(social_service_center__pk=request.GET['soc_service_id']).mentor
            mentor_data = model_to_dict(mentor, fields=(
                'first_name',
                'last_name',
                'status',
                'phone_number',
            ))
            mentor_data['email'] = mentor.user.email
            mentor_data['licence_key'] = mentor.licence_key.key
            mentor_data['date_of_birth'] = mentor.questionnaire.date_of_birth.strftime('%d.%m.%Y')
            mentor_data['age'] = get_age(mentor.questionnaire.date_of_birth)
            mentor_data['address'] = mentor.questionnaire.actual_address
            mentor_data['questionnaire_creation_date'] = formats.date_format(mentor.questionnaire.creation_date)
            return JsonResponse(mentor_data)

        return super().get(request, *args, **kwargs)
