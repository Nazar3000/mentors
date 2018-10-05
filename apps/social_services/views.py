from django.http import JsonResponse
from django.views.generic import TemplateView

from users.constants import MentorStatuses
from users.models import Mentor, PublicService


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

        return super().get(request, *args, **kwargs)
