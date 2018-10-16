import json

from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils import formats
from django.shortcuts import redirect, HttpResponse
from django.views.generic import TemplateView, FormView, DetailView, ListView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages

from social_services.utils import get_date_str_formatted
from .forms import SignUpStep0Form, AuthenticationForm, MentorSocialServiceCenterDataEditForm
from .models import SocialServiceVideo, Material, MaterialCategory
from users.models import Mentor
from mentors.models import MentorSocialServiceCenterData, MentorLicenceKey
from social_services.forms import MentorEditForm
from users.constants import MentorStatuses, UserTypes
from users.models import PublicService, Coordinator, SocialServiceCenter
from users.templatetags.date_tags import get_age

User = get_user_model()


class SignUpFormView(FormView):
    template_name = 'social_services/ssc_register.html'
    form_class = SignUpStep0Form

    def form_valid(self, form):
        form.save()
        return redirect('social_services:video')


class LoginView(FormView):
    template_name = 'social_services/ssc_login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
        else:
            messages.error(self.request, 'Невірний пароль.')
            return redirect('social_services:ssc_login')
        return redirect('/')


class MainPageView(TemplateView):
    template_name = 'social_services/ssc_main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['main_video'] = SocialServiceVideo.objects.filter(page=1).first()
        return context


class VideoMentorView(TemplateView):
    template_name = 'social_services/ssc_video_mentor.html'

    def get_context_data(self, **kwargs):
        context = super(VideoMentorView, self).get_context_data(**kwargs)
        context['mentor_video'] = SocialServiceVideo.objects.filter(page=2).first()
        return context


class MentorCardView(DetailView):
    model = Mentor
    template_name = 'social_services/ssc_mentor_card.html'


class MaterialView(ListView):
    model = Material
    template_name = 'social_services/ssc_material.html'

    def get_context_data(self, **kwargs):
        context = super(MaterialView, self).get_context_data(**kwargs)
        context['categories'] = MaterialCategory.objects.all()
        return context


def download_file(request, material_id):
    material = Material.objects.get(id=material_id)
    filename = material.file.name.split('/')[-1]
    response = HttpResponse(material.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


class MentorsView(TemplateView):
    template_name = 'social_services/mentors.html'

    @staticmethod
    def get_responsible_pk(coordinator_pk):
        coordinator = Coordinator.objects.get(pk=coordinator_pk)
        try:
            responsible = coordinator.social_service_center.pk
        except SocialServiceCenter.DoesNotExist:
            responsible = coordinator.public_service.pk
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
            'coordinator'
        )
        for data in mentors_data:
            mentor = Mentor.objects.get(pk=data['pk'])
            soc_service_data, created = MentorSocialServiceCenterData.objects.get_or_create(mentor=mentor)
            data['docs_status'] = soc_service_data.docs_status
            data['responsible'] = self.get_responsible_pk(data['coordinator'])

        return JsonResponse({
            'mentors_data': list(mentors_data),
            'mentor_statuses': mentor_statuses,
            'public_services': list(related_public_services)
        })

    def get_extended_data(self):
        mentor = Mentor.objects.get(pk=self.request.GET['mentor_id'])
        mentor_data = model_to_dict(mentor, fields=(
            'first_name',
            'last_name',
            'status',
            'phone_number',
        ))
        mentor_data['pk'] = mentor.pk
        mentor_data['email'] = mentor.user.email
        mentor_data['licence_key'] = mentor.licence_key.key
        mentor_data['date_of_birth'] = get_date_str_formatted(mentor.questionnaire.date_of_birth)
        mentor_data['address'] = mentor.questionnaire.actual_address
        mentor_data['questionnaire_creation_date'] = get_date_str_formatted(mentor.questionnaire.creation_date)
        mentor_data['responsible'] = self.get_responsible_pk(mentor.coordinator.pk)
        mentor_data['profile_image'] = mentor.profile_image.url if mentor.profile_image else ''

        mentor_social_service_center_data = model_to_dict(mentor.social_service_center_data)
        if mentor.social_service_center_data.infomeeting_date:
            mentor_social_service_center_data['infomeeting_date'] = \
                get_date_str_formatted(mentor.social_service_center_data.infomeeting_date)
        if mentor.social_service_center_data.psychologist_meeting_date:
            mentor_social_service_center_data['psychologist_meeting_date'] = \
                get_date_str_formatted(mentor.social_service_center_data.psychologist_meeting_date)
        if mentor.social_service_center_data.training_date:
            mentor_social_service_center_data['training_date'] = \
                get_date_str_formatted(mentor.social_service_center_data.training_date)
        if mentor.social_service_center_data.contract_date:
            mentor_social_service_center_data['contract_date'] = \
                get_date_str_formatted(mentor.social_service_center_data.contract_date)

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
        action = kwargs['action']
        if action == 'change_light_data':
            mentor = Mentor.objects.get(pk=request.POST['pk'])
            mentor.status = request.POST['status']
            coordinator = Coordinator.get_coordinator_by_related_service_pk(request.POST['responsible'])
            mentor.coordinator = coordinator
            mentor.save()
        elif action == 'change_extended_data':
            # edit/create mentor
            licence_key = request.POST['licence_key']
            instance = Mentor.objects.get(pk=request.POST['pk']) if request.POST.get('pk') else None
            form = MentorEditForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                mentor = form.save(commit=False)
                if mentor.licence_key:
                    mentor.licence_key.key = licence_key
                    mentor.licence_key.save()
                else:
                    key = MentorLicenceKey.objects.create(key=licence_key)
                    mentor.licence_key = key
                # if not request.POST.get('pk'):
                #     user_form = MentorUserForm(request.POST)
                #     if user_form.is_valid():
                #         user = user_form.save()
                #         mentor.user = user
                #         user.save()
                #     else:
                #         return JsonResponse(dict(user_form.errors.items()))
                mentor.save()
            else:
                return JsonResponse(dict(form.errors.items()))
        elif action == 'change_social_service_center_data':
            social_service_center_data_inst = MentorSocialServiceCenterData.objects.get(
                id=request.POST['id'])
            form = MentorSocialServiceCenterDataEditForm(request.POST,
                                                         instance=social_service_center_data_inst)
            if form.is_valid():
                social_service_center_data_obj = form.save(commit=False)
                social_service_center_data_obj.mentor = Mentor.objects.get(pk=request.POST['mentor'])
                social_service_center_data_obj.save()
            else:
                return JsonResponse(dict(form.errors.items()))

        return JsonResponse({'status': 'success'})
