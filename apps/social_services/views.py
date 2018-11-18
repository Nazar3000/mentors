from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, HttpResponse
from django.views.generic import TemplateView, FormView, DetailView, ListView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from mentors.constants import DocsStatuses
from social_services.utils import get_date_str_formatted
from .forms import SignUpStep0Form, AuthenticationForm, MentorSocialServiceCenterDataEditForm, PublicServiceEditForm
from .models import SocialServiceVideo, Material, MaterialCategory
from users.models import Mentor
from mentors.models import MentorSocialServiceCenterData, MentorLicenceKey, Mentoree
from social_services.forms import MentorEditForm
from users.constants import MentorStatuses, PublicServiceStatuses, UserTypes
from users.models import PublicService, Coordinator, SocialServiceCenter

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


class GetSocialServiceRelatedMentors:
    """
    Get specified fields from Mentor related to current SocialServiceCenter user
    """

    def get_mentors_query_data(self, fields_select_query):
        mentors_query_data = Mentor.objects.raw("""
            SELECT
                users_mentor.user_id,
                {fields_select_query}
            FROM users_mentor
                JOIN users_coordinator ON users_mentor.coordinator_id = users_coordinator.id
                JOIN mentors_mentorlicencekey ON users_mentor.licence_key_id = mentors_mentorlicencekey.id
            WHERE users_coordinator.social_service_center_id = '{current_soc_service_id}'
                OR users_coordinator.public_service_id 
                IN (SELECT user_id 
                    FROM users_publicservice 
                    WHERE users_publicservice.social_service_center_id = '{current_soc_service_id}')
        """.format(current_soc_service_id=self.request.user.id, fields_select_query=fields_select_query))
        return mentors_query_data


class MentorsView(GetSocialServiceRelatedMentors, TemplateView):
    template_name = 'social_services/mentors.html'

    @staticmethod
    def get_responsible_pk(coordinator_pk):
        coordinator = Coordinator.objects.get(pk=coordinator_pk)
        try:
            responsible = coordinator.social_service_center.pk
        except AttributeError:
            try:
                responsible = coordinator.public_service.pk
            except AttributeError:
                responsible = None
        return responsible

    def get_light_data(self):
        mentor_statuses = dict(MentorStatuses.choices())
        related_public_services = PublicService.objects.filter(
            social_service_center__pk=self.request.user.pk).values('pk', 'name')
        mentors_query_data = self.get_mentors_query_data(
            """
                users_mentor.first_name || ' ' || users_mentor.last_name as full_name,
                users_mentor.phone_number,
                mentors_mentorlicencekey.key as licence_key__key,
                users_mentor.status,
                users_mentor.coordinator_id,
                (CASE WHEN (users_coordinator.social_service_center_id IS NOT NULL )
                 THEN users_coordinator.social_service_center_id
                 ELSE users_coordinator.public_service_id END
                 ) as responsible
            """
        )

        mentors_data = []
        for mentor in mentors_query_data.iterator():
            mentor_dict = mentor.__dict__
            soc_service_data, created = MentorSocialServiceCenterData.objects.get_or_create(mentor=mentor)
            mentor_dict['docs_status'] = soc_service_data.docs_status
            mentor_dict['pk'] = mentor.pk
            del mentor_dict['_state']
            mentors_data.append(mentor_dict)

        return JsonResponse({
            'mentors_data': mentors_data,
            'mentor_statuses': mentor_statuses,
            'docs_statuses': dict(DocsStatuses.choices()),
            'public_services': list(related_public_services)
        })

    def get_extended_data(self):
        mentor = Mentor.objects.get(pk=self.request.GET['mentor_id'])
        mentor_data = model_to_dict(mentor, fields=(
            'first_name',
            'last_name',
            'status',
            'phone_number',
            'actual_address',
            'date_of_birth',
        ))
        mentor_data['pk'] = mentor.pk
        mentor_data['email'] = mentor.user.email
        mentor_data['licence_key'] = mentor.licence_key.key
        mentor_data['responsible'] = self.get_responsible_pk(mentor.coordinator.pk)
        mentor_data['date_of_birth'] = get_date_str_formatted(mentor.date_of_birth)
        mentor_data['profile_image'] = mentor.profile_image.url if mentor.profile_image else ''
        mentor_data['questionnaire_creation_date'] = get_date_str_formatted(mentor.questionnaire_creation_date)

        mentor_social_service_center_data = model_to_dict(mentor.social_service_center_data)

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


class PublicServicesView(GetSocialServiceRelatedMentors, TemplateView):
    template_name = 'social_services/public_services.html'

    def get_light_public_service_data(self):
        mentors_query_data = self.get_mentors_query_data(
            """
                users_mentor.first_name || ' ' || users_mentor.last_name as full_name,
                mentoree_id
            """
        )
        mentor_list = list(map(lambda m: {'pk': m.pk, 'full_name': m.full_name}, mentors_query_data.iterator()))
        mentoree_ids = []
        for mentor in mentors_query_data:
            mentoree_ids.append(mentor.mentoree_id)
        organization_list = Mentoree.objects.filter(pk__in=mentoree_ids) \
            .distinct().values('organization__pk', 'organization__name')

        service_data = PublicService.objects.filter(social_service_center__pk=self.request.user.id) \
            .values('pk', 'name', 'status')
        for data in service_data:
            service = PublicService.objects.get(pk=data['pk'])
            data['pair_count'] = service.pair_count
            data['licence'] = service.licence

        return JsonResponse({
            'mentor_list': mentor_list,
            'organization_list': list(organization_list),
            'service_data': list(service_data),
            'public_service_statuses': dict(PublicServiceStatuses.choices()),
        })

    def get_extended_public_service_data(self):
        public_service = PublicService.objects.get(pk=self.request.GET['public_service_pk'])
        public_service_data = model_to_dict(public_service, fields=(
            'name',
            'max_pair_count',
            'phone_number',
            'email',
            'address',
            'website',
            'contract_number',
            'licence',
        ))
        public_service_data['pk'] = public_service.pk
        public_service_data['profile_image'] = public_service.profile_image.url
        public_service_data['pair_count'] = public_service.pair_count

        coordinator_ids = PublicService.objects.filter(social_service_center__pk=self.request.user.pk)\
            .values_list('coordinators', flat=True)
        mentor_pks = Coordinator.objects.filter(id__in=coordinator_ids).values_list('mentors__pk', flat=True)
        mentors_data = []
        mentors = Mentor.objects.filter(pk__in=mentor_pks).iterator()

        related_public_services = PublicService.objects.filter(
            social_service_center__pk=self.request.user.pk).values('pk', 'name')
        for mentor in mentors:
            mentors_data.append({
                'pk': mentor.pk,
                'full_name': mentor.first_name + ' ' + mentor.last_name,
                'mentoree_full_name': '{} {}'.format(mentor.mentoree.first_name, mentor.mentoree.last_name),
                'organization_name': mentor.mentoree.organization.name,
                'contract_number': mentor.social_service_center_data.contract_number,
                'mentoring_start_date':
                    get_date_str_formatted(mentor.meetings.first().date()) if mentor.meetings.first() else None,
            })

        return JsonResponse({
            'public_service_data': public_service_data,
            'mentor_statuses': dict(MentorStatuses.choices()),
            'public_services': list(related_public_services),
            'mentors_data': mentors_data
        })

    def get(self, request, *args, **kwargs):
        if 'get_light_public_service_data' in request.GET.keys():
            return self.get_light_public_service_data()

        elif 'get_extended_public_service_data' in request.GET.keys():
            return self.get_extended_public_service_data()

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        action = kwargs['action']
        if action == 'change_light_data':
            public_service = PublicService.objects.get(pk=request.POST['pk'])
            public_service.status = request.POST['status']
            public_service.save()
        elif action == 'change_extended_data':
            # edit/create public service
            instance = PublicService.objects.get(pk=request.POST['pk']) if request.POST.get('pk') else None
            form = PublicServiceEditForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                public_service = form.save(commit=False)
                if not instance:
                    public_service.social_service_center_id = request.user.pk
                    public_service.status = request.POST['status']
                    if not User.objects.filter(email=form.cleaned_data['email']).exists():
                        user = User.objects.create_user(email=form.cleaned_data['email'])
                        user.user_type = UserTypes.PUBLIC_SERVICE
                        public_service.user = user
                    else:
                        return JsonResponse(
                            {'non_field_errors': [_('Користувач з таким email же існує.')]})
                public_service.save()
            else:
                return JsonResponse(dict(form.errors.items()))
        return JsonResponse({'status': 'success'})


class DatingView(TemplateView):
    template_name = 'social_services/ssc_dating.html'
