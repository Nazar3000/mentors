import json
import rstr

from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.forms import model_to_dict

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, DetailView, ListView

from govern_users.models import MentorSchoolVideo, MentorTip
from users.constants import UserTypes
from users.templatetags.date_tags import get_time_spent, get_age
from .models import MentorLicenceKey, Mentoree, Post, PostComment
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
        # TODO: replace ?
        context['mentor_school_videos'] = \
            MentorSchoolVideo.objects.order_by('?')[:2]
        context['mentor_tip'] = MentorTip.objects.order_by('?').first()
        context['last_post'] = self.object.posts.last()
        return context


class MentorSchoolVideoListView(CheckIfUserIsMentorMixin, ListView):
    template_name = 'mentors/mentor_school_video_list.html'
    queryset = MentorSchoolVideo.objects.all()

    def get_queryset(self):
        nested_videos = []
        nest_size = 4
        for index, vid in enumerate(MentorSchoolVideo.objects.all(), 1):
            if (index + nest_size) % nest_size == 1:
                nested_videos.append([])
                nested_videos[index // nest_size].append(vid)
            else:
                nested_index = index // nest_size - 1 \
                    if index // nest_size == 1 else index // nest_size
                nested_videos[nested_index].append(vid)
        return nested_videos

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['mentor_user'] = Mentor.objects.get(pk=self.request.user.pk)
        return context

    def post(self, *args, **kwargs):
        video = MentorSchoolVideo.objects.get(id=self.request.POST['video_id'])
        if self.request.user.pk in video.watched_by.all().values_list('pk', flat=True):
            video.watched_by.remove(self.request.user.pk)
        else:
            video.watched_by.add(self.request.user.pk)
        return JsonResponse({})


class MentorSchoolVideoDetailView(CheckIfUserIsMentorMixin, DetailView):
    template_name = 'mentors/mentor_school_video_detail.html'
    model = MentorSchoolVideo


class MentoreeDetailView(CheckIfUserIsMentorMixin, TemplateView):
    template_name = 'mentors/mentoree_detail.html'

    def get(self, *args, **kwargs):
        if 'get_mentoree_data' in self.request.GET.keys():
            model_dict = model_to_dict(self.get_object())
            if model_dict.get('profile_image'):
                model_dict['profile_image'] = model_dict['profile_image'].url
            model_dict['organization'] = model_to_dict(
                self.get_object().organization,
                fields=['name', 'address', 'phone_numbers'])
            model_dict['date_of_birth'] = self.get_object().date_of_birth.strftime('%d.%m.%Y')
            model_dict['age'] = get_age(self.get_object().date_of_birth)
            return JsonResponse(model_dict)
        return super().get(*args, **kwargs)

    def get_object(self, queryset=None):
        return Mentor.objects.get(pk=self.request.user.pk).mentoree

    def post(self, *args, **kwargs):
        if 'extra_fields_data' in self.request.POST.keys():
            jdata = json.loads(self.request.POST['data'])
            mentoree = Mentor.objects.get(pk=self.request.POST['user_id']).mentoree
            mentoree.extra_data_fields = jdata
            mentoree.save()
        print(self.request.POST)
        return JsonResponse({})


class PostListView(CheckIfUserIsMentorMixin, ListView):
    template_name = 'mentors/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(related_user__pk=self.request.user.pk)


def send_post_comment(request):
    comment = PostComment.objects.create(
        post_id=request.POST['post_id'],
        author_id=request.user.id,
        content=request.POST['comment'])
    return JsonResponse({
        'author_full_name': ' '.join([comment.author.first_name, comment.author.last_name]),
        'author_profile_image': comment.author.profile_image.url,
        'date_time': get_time_spent(comment.datetime)})
