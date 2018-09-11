import json
import rstr
from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, DetailView, ListView
from django.conf import settings

from govern_users.models import MentorSchoolVideo, MentorTip
from users.constants import UserTypes
from users.templatetags.date_tags import get_time_spent, get_age
from .models import MentorLicenceKey, Post, PostComment, StoryImage, Meeting, MeetingImage
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

    @staticmethod
    def nest_queryset(nest_size):
        """
        Return list of list with same length
        """
        nested_videos = []
        for index, vid in enumerate(MentorSchoolVideo.objects.all(), 1):
            if (index + nest_size) % nest_size == 1:
                nested_videos.append([])
                nested_videos[index // nest_size].append(vid)
            else:
                nested_index = index // nest_size - 1 \
                    if index // nest_size == 1 else index // nest_size
                nested_videos[nested_index].append(vid)
        return nested_videos

    def get_queryset(self):
        return self.nest_queryset(nest_size=4)

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
            if self.get_object():
                model_dict = model_to_dict(self.get_object())
                if model_dict.get('profile_image'):
                    model_dict['profile_image'] = model_dict['profile_image'].url
                model_dict['organization'] = model_to_dict(
                    self.get_object().organization,
                    fields=['name', 'address', 'phone_numbers'])
                model_dict['date_of_birth'] = self.get_object().date_of_birth.strftime('%d.%m.%Y')
                model_dict['age'] = get_age(self.get_object().date_of_birth)
                model_dict['story_images'] = list(
                    map(lambda img: img.image.url, (self.get_object().story_images.all())))
                return JsonResponse(model_dict)
            else:
                return JsonResponse({'status': 'no_related_mentoree_found'})
        return super().get(*args, **kwargs)

    def get_object(self, queryset=None):
        return Mentor.objects.get(pk=self.request.user.pk).mentoree

    def post(self, *args, **kwargs):
        mentoree = Mentor.objects.get(pk=self.request.POST['user_id']).mentoree
        if 'extra_fields_data' in self.request.POST.keys():
            jdata = json.loads(self.request.POST['extra_fields_data']['data'])
            mentoree.extra_data_fields = jdata
            mentoree.save()
        elif 'mentoree_data' in self.request.POST.keys():
            mentoree_data = self.request.POST

            mentoree.first_name = mentoree_data['first_name']
            mentoree.last_name = mentoree_data['last_name']
            mentoree.date_of_birth = datetime.strptime(mentoree_data['date_of_birth'], '%d.%m.%Y')
            mentoree.dream = mentoree_data['dream']
            mentoree.want_to_become = mentoree_data['want_to_become']
            mentoree.fears = mentoree_data['fears']
            mentoree.loves = mentoree_data['loves']
            mentoree.hates = mentoree_data['hates']
            mentoree.strengths = mentoree_data['strengths']
            mentoree.extra_data = mentoree_data['extra_data']
            if 'profile_image' in self.request.FILES.keys() \
                    and 'profile_image' not in mentoree_data.keys():
                mentoree.profile_image.save(
                    self.request.FILES['profile_image'].name,
                    self.request.FILES['profile_image'])
            mentoree.save()
        elif 'mentoree_story' in self.request.POST.keys():
            mentoree.story = self.request.POST['story']
            mentoree.save()

            old_images = list(map(
                lambda img: img.split(settings.MEDIA_URL)[1],
                self.request.POST['old_images'].split(',')))
            StoryImage.objects.exclude(
                image__in=old_images).delete()
            for i in range(len(self.request.FILES)):
                story_image = StoryImage(mentoree_id=mentoree.pk)
                story_image.image.save(
                    self.request.FILES['new_image_{}'.format(i)].name,
                    self.request.FILES['new_image_{}'.format(i)],
                    save=True)

        return JsonResponse({'status': 'success'})


class PostListView(CheckIfUserIsMentorMixin, ListView):
    template_name = 'mentors/post_list.html'

    def get_queryset(self):
        return Post.objects.all().order_by('-datetime')

    def get_queryset_dict_list(self, post_queryset):
        queryset_dict_list = []
        for post in post_queryset.iterator():
            post_dict = model_to_dict(post, fields=('id', 'content',))
            post_dict['author'] = model_to_dict(
                post.author,
                fields=('id', 'first_name', 'last_name',))
            post_dict['author']['profile_image'] = post.author.profile_image.url
            post_dict['likes'] = post.likes.count()
            if post.image:
                post_dict['image'] = post.image.url
            post_dict['datetime'] = get_time_spent(post.datetime)

            comments = post.comments.all()
            post_dict['comments'] = []
            for comment in comments:
                comment_dict = model_to_dict(comment, fields=(
                    'id', 'author', 'datetime', 'content'))
                comment_dict['datetime'] = get_time_spent(comment.datetime)
                comment_dict['author'] = model_to_dict(
                    comment.author,
                    fields=('first_name', 'last_name',))
                comment_dict['author']['id'] = comment.author.pk
                comment_dict['author']['profile_image'] = comment.author.profile_image.url
                post_dict['comments'].append(comment_dict)

            queryset_dict_list.append(post_dict)
        return queryset_dict_list

    def get(self, request, *args, **kwargs):
        if 'get_posts' in request.GET.keys():
            queryset_dict_list = self.get_queryset_dict_list(self.get_queryset())
            return JsonResponse(queryset_dict_list, safe=False)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        if 'new_post' in request.POST.keys():
            post = Post(
                author_id=request.user.pk,
                content=request.POST['text']
            )
            if 'image' in self.request.FILES:
                post.image.save(
                    self.request.FILES['image'].name,
                    self.request.FILES['image'],
                    save=False)
            post.save()
            post_list = self.get_queryset_dict_list(
                Post.objects.filter(id=post.id))
            return JsonResponse(post_list, safe=False)

        return JsonResponse({'status': 'success'})


def send_post_comment(request):
    comment = PostComment.objects.create(
        post_id=request.POST['post_id'],
        author_id=request.user.id,
        content=request.POST['comment'])
    return JsonResponse({
        'author_full_name': ' '.join([comment.author.first_name, comment.author.last_name]),
        'author_profile_image': comment.author.profile_image.url,
        'date_time': get_time_spent(comment.datetime)})


class MeetingListView(CheckIfUserIsMentorMixin, ListView):
    template_name = 'mentors/meeting_list.html'

    def get_queryset(self):
        return Meeting.objects.filter(performer__pk=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        if 'get_meetings_data' in self.request.GET.keys():
            meeting_query_list = self.get_queryset().values(
                'id',
                'title',
                'date',
                'description',
                'observation',
                'note_for_next_meeting',)
            meeting_list = []
            for meeting in meeting_query_list.iterator():
                meeting['date'] = datetime.strftime(meeting['date'], '%d. %m. %Y')
                meeting['images'] = []
                for image in MeetingImage.objects.filter(meeting_id=meeting['id']).iterator():
                    meeting['images'].append(image.image.url)
                meeting_list.append(meeting)
            return JsonResponse(meeting_list, safe=False)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'delete_meeting' in self.request.POST.keys():
            Meeting.objects.get(id=self.request.POST['meeting_id']).delete()
        return JsonResponse({'status': 'success'})


def like_news_item(request):
    post = Post.objects.get(id=request.POST['post_id'])
    if request.user.id in post.likes.all().values_list('user_id', flat=True):
        post.likes.remove(request.user.id)
    else:
        post.likes.add(request.user.id)
    return JsonResponse({'likes': post.likes.count()})
