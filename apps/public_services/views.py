from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from social_services.forms import DatingCoordinatorForm
from social_services.models import BaseSocialServiceCenter
from social_services.views import SignUpFormView, DatingView
from users.models import PublicService
from .forms import PublicOrganizationSignUpStep0Form
from django.views.generic import TemplateView
from .models import PublicServiceVideo


class PublicServiceSignUpFormView(SignUpFormView):
    form_class = PublicOrganizationSignUpStep0Form

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
    form_class = DatingCoordinatorForm

    def get_queryset(self, q_filter):
        return BaseSocialServiceCenter.objects.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'data' in kwargs.keys():
            kwargs['data'] = dict(kwargs['data'])
            if 'coordinator_phone_numbers' in kwargs['data'].keys():
                kwargs['data']['phone_numbers'] = kwargs['data']['coordinator_phone_numbers']
                kwargs['data']['email'] = kwargs['data']['email'][0]
        return kwargs

    def form_valid(self, form):
        if 'pk' in self.request.POST.keys():
            service = BaseSocialServiceCenter.objects.get(pk=self.request.POST['pk']).service
            if service is not None:
                public_service = PublicService.objects.create(
                    user=self.request.user,
                    social_service_center=service)

                coordinator = form.save(commit=False)
                coordinator.public_service = public_service
                coordinator.save()

                return JsonResponse({'status': 'success'})
            else:
                JsonResponse({'non_field_errors': _('Обраний ЦСССДМ не зареєстрований.')})
        return JsonResponse({'non_field_errors': _('Оберіть центр зі списку')})

    def form_invalid(self, form):
        errs = dict(form.errors.items())
        if 'phone_numbers' in errs.keys():
            errs['coordinator_phone_numbers'] = errs['phone_numbers']
        return JsonResponse(errs)


class PublicServiceMainPageView(TemplateView):
    template_name = 'public_services/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_video'] = PublicServiceVideo.objects.filter(page=1).first()
        return context
