import json
import rstr
from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.forms import model_to_dict, formset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, DetailView, ListView
from django.conf import settings

from govern_users.models import MentorSchoolVideo, MentorTip
from users.constants import UserTypes
from users.templatetags.date_tags import get_time_spent, get_age
from .models import MentorLicenceKey, Post, PostComment, StoryImage, Meeting, MeetingImage, Mentoree
from users.models import Mentor, Organization
from .forms import SignUpStep0Form, SignUpStep1Form, SignUpStep2Forms, MeetingForm, MentoreeEditForm
from .constants import Religions, MaritalStatuses, Genders, HomeTypes, AbleToVisitChildFrequency, \
    MentoringProgramFindOutPlaces, EducationTypes, LocalChurchVisitingFrequency


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


class SignUpStep2View(SignUpStepsAccessMixin, View):
    template_name = 'mentors/signup_step2.html'
    forms_class = SignUpStep2Forms
    success_url = reverse_lazy('mentors:mentor_roadmap')

    def get(self, request, *args, **kwargs):
        if 'get_selector_choices' in request.GET.keys():
            choices_dicts = dict(
                religions=dict(Religions.choices()),
                local_church_visiting_frequency=dict(LocalChurchVisitingFrequency.choices()),
                marital_statuses=dict(MaritalStatuses.choices()),
                genders=dict(Genders.choices()),
                home_types=dict(HomeTypes.choices()),
                able_to_visit_child_frequency=dict(AbleToVisitChildFrequency.choices()),
                mentoring_program_find_out_places=dict(MentoringProgramFindOutPlaces.choices()),
                education_types=dict(EducationTypes.choices()))
            return JsonResponse(choices_dicts)
        return render(request, self.template_name, {'forms': self.forms_class.forms})

    def post(self, request, *args, **kwargs):
        request_body = json.loads(request.body)

        errors = {}

        main_form = self.forms_class.forms['main'](request_body)
        questionnaire = None
        if main_form.is_valid():
            questionnaire = main_form.save(commit=False)
            questionnaire.mentor = Mentor.objects.filter(pk=request.user.pk)
            questionnaire.save()
        else:
            errors.update(dict(main_form.errors.items()))

        for form_name in [
                'education',
                'job',
                'family_member',
                'children_work_experience']:
            error_list = []
            for i in range(len(request_body[form_name + 's'])):
                form = self.forms_class.forms[form_name](request_body[form_name + 's'][i])
                if form.is_valid():
                    if questionnaire:
                        q_object = form.save(commit=False)
                        q_object.questionnaire = questionnaire
                        q_object.save()

                    error_list.append({})
                else:
                    error_list.append(dict(form.errors.items()))
            errors[form_name + 's'] = error_list

        has_errors = False
        for value in errors.values():
            if (type(value) == list and any(len(d) > 0 for d in value)
                    or type(value) == str and len(value) > 0):
                has_errors = True

        if has_errors:
            if questionnaire:
                questionnaire.delete()
            return JsonResponse(errors)

        return JsonResponse({'status': 'success'})


class SignUpStep3View(SignUpStepsAccessMixin, TemplateView):
    template_name = 'mentors/signup_step3.html'


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
    mentoree_edit_form = MentoreeEditForm

    def get(self, *args, **kwargs):
        model_dict = dict()
        model_dict['all_organizations'] = list(
            Organization.objects.all().values('id', 'name', 'address', 'phone_numbers'))

        if 'get_mentoree_data' in self.request.GET.keys():
            mentoree = self.get_object()
            if mentoree:
                model_dict.update(model_to_dict(
                    mentoree,
                    exclude=('profile_image', 'organization', 'date_of_birth',)))
                model_dict['profile_image'] = mentoree.profile_image.url
                if mentoree.organization:
                    model_dict['organization'] = mentoree.organization.id

                model_dict['date_of_birth'] = mentoree.date_of_birth.strftime('%d.%m.%Y')
                model_dict['age'] = get_age(mentoree.date_of_birth)
                model_dict['story_images'] = list(
                    map(lambda img: img.image.url, (mentoree.story_images.all())))
                return JsonResponse(model_dict)
            else:
                return JsonResponse(model_dict)
        return super().get(*args, **kwargs)

    def get_object(self):
        return Mentor.objects.get(pk=self.request.user.pk).mentoree

    def post(self, *args, **kwargs):
        mentoree = Mentor.objects.get(pk=self.request.POST['user_id']).mentoree
        if 'extra_fields_data' in self.request.POST.keys():
            jdata = json.loads(self.request.POST['extra_fields_data'])
            mentoree.extra_data_fields = jdata
            mentoree.save()
        elif 'mentoree_data' in self.request.POST.keys():
            mentor = Mentor.objects.get(pk=self.request.POST['user_id'])
            mentoree_edit_form = self.mentoree_edit_form(
                self.request.POST, self.request.FILES, instance=mentor.mentoree)
            if mentoree_edit_form.is_valid():
                mentoree = mentoree_edit_form.save(commit=False)
                mentoree.organization_id = self.request.POST['organization_id']
                mentoree.save()

                mentor.mentoree = mentoree
                mentor.save()
            else:
                return JsonResponse(dict(mentoree_edit_form.errors.items()))
        elif 'mentoree_story' in self.request.POST.keys():
            mentoree.story = self.request.POST['story']
            mentoree.save()

            if self.request.POST['old_images']:
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
            if post.author.profile_image:
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
                if comment.author.profile_image:
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
    comment_dict = model_to_dict(comment, fields=('content', 'datetime', 'id',))
    comment_dict['author'] = model_to_dict(
        comment.author,
        fields=('first_name', 'last_name', 'id',))

    if comment.author.profile_image:
        comment_dict['author']['profile_image'] = comment.author.profile_image.url
    return JsonResponse(comment_dict)


class MeetingListView(CheckIfUserIsMentorMixin, TemplateView):
    template_name = 'mentors/meeting_list.html'
    form_class = MeetingForm

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
        elif 'image_data' in self.request.POST.keys():
            image = MeetingImage(meeting_id=self.request.POST['meeting_id'])
            image.image.save(
                self.request.FILES['image'].name,
                self.request.FILES['image'])

        return JsonResponse({'status': 'success'})


def like_news_item(request):
    post = Post.objects.get(id=request.POST['post_id'])
    if request.user.id in post.likes.all().values_list('user_id', flat=True):
        post.likes.remove(request.user.id)
    else:
        post.likes.add(request.user.id)
    return JsonResponse({'likes': post.likes.count()})
