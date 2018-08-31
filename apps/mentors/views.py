import rstr
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DetailView, ListView

from govern_users.models import MentorSchoolVideo, MentorTip
from users.constants import UserTypes
from .models import MentorLicenceKey, Mentoree
from users.models import Mentor
from .forms import SignUpStep0Form, SignUpStep1Form, SignUpStep3Form


class SignUpStepsAccessMixin(AccessMixin):
    """
    Mixin to forbid users to skip registration steps.
    """
    def test_session_mentor_data(self):
        return ('mentor_data' in self.request.session.keys()) or self.request.user.is_authenticated

    def dispatch(self, request, *args, **kwargs):
        test_session_mentor_data_result = self.test_session_mentor_data()
        if not test_session_mentor_data_result:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class SignUpStep0View(FormView):
    template_name = 'mentors/signup_step0.html'
    form_class = SignUpStep0Form
    success_url = reverse_lazy('mentors:signup_step1')

    def form_valid(self, form):
        self.request.session['mentor_data'] = form.cleaned_data
        return HttpResponseRedirect(self.get_success_url())


class SignUpStep1View(SignUpStepsAccessMixin, FormView):
    template_name = 'mentors/signup_step1.html'
    form_class = SignUpStep1Form
    success_url = reverse_lazy('mentors:signup_step2')

    def get_initial(self):
        initial = super().get_initial()
        if 'mentor_data' in self.request.session.keys():
            initial['email'] = self.request.session['mentor_data']['email']
            del self.request.session['mentor_data']['email']
        return initial

    def form_valid(self, form):
        user = form.save()
        if 'mentor_data' in self.request.session.keys():
            mentor = Mentor(**self.request.session['mentor_data'])
            mentor.user = user
            mentor.licence_key = MentorLicenceKey.objects\
                .create(mentor=mentor, key=rstr.xeger(MentorLicenceKey.key_validator.regex))
            mentor.save()

            login(self.request, user)

        else:
            return redirect('mentors:signup_step0')
        return HttpResponseRedirect(self.get_success_url())


class SignUpStep2View(SignUpStepsAccessMixin, TemplateView):
    template_name = 'mentors/signup_step2.html'


class SignUpStep3View(SignUpStepsAccessMixin, FormView):
    # TODO: complete this view
    template_name = 'mentors/signup_step3.html'
    form_class = SignUpStep3Form
    success_url = reverse_lazy('mentors:mentor_roadmap')


class MentorRoadmap(TemplateView):
    template_name = 'mentors/mentor_roadmap.html'


class CheckIfUserIsMentorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == UserTypes.MENTOR


class MentorOfficeView(CheckIfUserIsMentorMixin, DetailView):
    template_name = 'mentors/mentor_office.html'
    model = Mentor

    def get_object(self, queryset=None):
        return Mentor.objects.get(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentor_school_videos'] = \
            MentorSchoolVideo.objects.all()[:2]
        context['mentor_tip'] = MentorTip.objects.order_by('?').first()
        return context


class MentorSchoolVideoListView(ListView):
    template_name = 'mentors/mentor_school_video.html'
    queryset = MentorSchoolVideo.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mentor'] = Mentor.objects.get(pk=self.request.user.pk)
        return context


class MentoreeDetailView(CheckIfUserIsMentorMixin, DetailView):
    template_name = 'mentors/mentoree_detail.html'
    model = Mentoree

    def get_object(self, queryset=None):
        return Mentor.objects.get(pk=self.request.user.pk).mentoree
