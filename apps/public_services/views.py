from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from social_services.models import BaseSocialServiceCenter
from social_services.views import SignUpFormView, DatingView, MainPageView, MentorsView, MentorCardView, MaterialView
from users.constants import UserTypes
from users.models import SocialServiceCenter, PublicService, Mentor
from .forms import PublicServiceSignUpStep0Form, PublicServiceForm
from django.views.generic import TemplateView
from .models import PublicServiceVideo


class CheckIfUserIsPublicServiceMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            PublicService.objects.get(user=self.request.user)
            return self.request.user.user_type == UserTypes.PUBLIC_SERVICE
        except (PublicService.DoesNotExist, TypeError):
            return False


class PublicServiceSignUpFormView(SignUpFormView):
    form_class = PublicServiceSignUpStep0Form

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('public_services:video')


class PublicServiceVideoMentorView(TemplateView):
    template_name = 'public_services/video_mentor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentor_video'] = PublicServiceVideo.objects.filter(page=2).first()
        return context


class PublicServiceDatingView(DatingView):
    template_name = 'public_services/dating.html'
    form_class = PublicServiceForm

    def get_queryset(self, q_filter):
        return BaseSocialServiceCenter.objects.all()

    def form_valid(self, form):
        if 'pk' in self.request.POST.keys():
            service = BaseSocialServiceCenter.objects.get(pk=self.request.POST['pk']).service
            if service is None:
                return JsonResponse({'non_field_errors': [_('Обраний ЦСССДМ ще не зареєстрований.')]})

            public_service = form.save(commit=False)
            public_service.user = self.request.user
            public_service.social_service_center = service
            public_service.save()

            data = {
                'phone_numbers': self.request.POST.get('coordinator_phone_numbers'),
                'email': self.request.POST.get('email'),
                'full_name': self.request.POST.get('coordinator_phone_numbers')
            }
            coordinator_form = self.coordinator_form_class(data)

            if coordinator_form.is_valid():
                coordinator = coordinator_form.save(commit=False)
                coordinator.public_service = public_service
                coordinator.save()
            else:
                errs = dict(coordinator_form.errors.items())
                if 'phone_numbers' in errs.keys():
                    errs['coordinator_phone_numbers'] = errs['phone_numbers']
                    del errs['phone_numbers']
                return JsonResponse(errs)
        else:
            return JsonResponse({'non_field_errors': [_('Оберіть центр зі списку')]})
        return JsonResponse({'status': 'success'})


class PublicServiceMainPageView(CheckIfUserIsPublicServiceMixin, MainPageView):
    template_name = 'public_services/main.html'

    def get_object(self):
        return SocialServiceCenter.objects.get(publicservice__pk=self.request.user.pk)

    def get_main_video(self):
        return PublicServiceVideo.objects.filter(page=1).first()


class PublicServiceMentorsView(CheckIfUserIsPublicServiceMixin, MentorsView):
    template_name = 'public_services/mentors.html'

    def get_mentors_query_data(self, fields_select_query):
        mentors_query_data = Mentor.objects.raw("""
            SELECT
                users_mentor.user_id,
                {fields_select_query}
            FROM users_mentor
                JOIN users_coordinator ON users_mentor.coordinator_id = users_coordinator.id
                JOIN mentors_mentorlicencekey ON users_mentor.licence_key_id = mentors_mentorlicencekey.id
            WHERE users_coordinator.public_service_id = '{current_pub_service_id}'
        """.format(current_pub_service_id=self.request.user.id, fields_select_query=fields_select_query))
        return mentors_query_data


class PublicServiceMentorCardView(CheckIfUserIsPublicServiceMixin, MentorCardView):
    pass


class PublicServiceMaterialView(MaterialView):
    template_name = 'public_services/material.html'
