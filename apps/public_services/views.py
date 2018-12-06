from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from social_services.models import BaseSocialServiceCenter
from social_services.views import SignUpFormView, DatingView
from .forms import PublicServiceSignUpStep0Form, PublicServiceForm
from django.views.generic import TemplateView
from .models import PublicServiceVideo


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


class PublicServiceMainPageView(TemplateView):
    template_name = 'public_services/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_video'] = PublicServiceVideo.objects.filter(page=1).first()
        return context
