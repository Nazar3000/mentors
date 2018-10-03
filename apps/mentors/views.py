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
from django.views.generic import TemplateView, FormView, DetailView, ListView, UpdateView, CreateView
from django.conf import settings

from govern_users.models import MentorSchoolVideo, MentorTip, TipOfTheDay
from users.constants import UserTypes
from users.templatetags.date_tags import get_time_spent, get_age
from .models import MentorLicenceKey, Post, PostComment, StoryImage, Meeting, MeetingImage, Proforientation
from users.models import Mentor, Organization, SocialServiceCenterAssessment, Coordinator, SocialServiceCenter
from .forms import SignUpStep0Form, SignUpStep1Form, SignUpStep2Forms, MeetingForm, MentoreeEditForm, PostForm, \
    MentorSettingsForm, MentorQuestionnaireSettingsForm, SscReportForm, SscAssessForm, ProforientationForm
from .constants import Religions, MaritalStatuses, Genders, HomeTypes, AbleToVisitChildFrequency, \
    MentoringProgramFindOutPlaces, EducationTypes, LocalChurchVisitingFrequency


def nest_queryset(nest_size, queryset):
    """
    Return list of list with same length
    """
    nested_items = []
    for index, item in enumerate(queryset, 1):
        if (index + nest_size) % nest_size == 1:
            nested_items.append([])
            nested_items[index // nest_size].append(item)
        else:
            nested_index = index // nest_size - 1 \
                if index // nest_size == 1 else index // nest_size
            nested_items[nested_index].append(item)
    return nested_items


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
            mentor.licence_key = MentorLicenceKey.objects \
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
            'children_work_experience'
        ]:
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


class Roadmap(TemplateView):
    # TODO: complete all roadmap steps
    template_name = 'mentors/roadmap.html'


class RoadmapStepMixin(TemplateView):
    def post(self, request, *args, **kwargs):
        licence_key = request.POST['licence_key']
        mentor = Mentor.objects.get(pk=self.request.user.pk)
        if Mentor.objects.get(pk=self.request.user.pk).licence_key.key == licence_key:
            mentor.licenced = True
            mentor.save()
            return redirect('mentors:mentor_office')
        else:
            return self.get(request, *args, **kwargs)


class RoadmapStep1(RoadmapStepMixin):
    template_name = 'mentors/roadmap_step1.html'


class RoadmapStep2(RoadmapStepMixin):
    template_name = 'mentors/roadmap_step2.html'


class RoadmapStep3(RoadmapStepMixin):
    template_name = 'mentors/roadmap_step3.html'


class CheckIfUserIsMentorMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            mentor = Mentor.objects.get(user=self.request.user)
            return self.request.user.user_type == UserTypes.MENTOR and mentor.licenced
        except Mentor.DoesNotExist:
            return False


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
        context['last_post'] = Post.objects.last()
        return context


def get_next_tip(request):
    next_tip = MentorTip.objects.exclude(id=request.GET['id']).order_by('?').first()
    next_tip_dict = {
        'id': next_tip.id,
        'title': next_tip.title,
        'content': next_tip.content,
        'image': next_tip.image.url
    }
    return JsonResponse(next_tip_dict)


class MentorSchoolVideoListView(CheckIfUserIsMentorMixin, ListView):
    template_name = 'mentors/mentor_school_video_list.html'
    queryset = MentorSchoolVideo.objects.all()

    def get_queryset(self):
        return nest_queryset(4, MentorSchoolVideo.objects.all())

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
                if mentoree.profile_image:
                    model_dict['profile_image'] = mentoree.profile_image.url
                if mentoree.organization:
                    model_dict['organization'] = mentoree.organization.id

                if mentoree.date_of_birth:
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
    form_class = PostForm

    def get_queryset(self):
        return Post.objects.all().order_by('-datetime')

    def get_queryset_dict_list(self, post_queryset):
        queryset_dict_list = []
        for post in post_queryset.iterator():
            post_dict = model_to_dict(post, fields=('id', 'content',))
            post_dict['author'] = model_to_dict(
                post.author,
                fields=('user', 'first_name', 'last_name',))
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
            if 'id' in request.POST.keys():
                instance = Post.objects.get(id=request.POST['id'])
            else:
                instance = None
            form = self.form_class(request.POST, self.request.FILES, instance=instance)
            if form.is_valid():
                post = form.save(commit=False)
                post.author_id = self.request.user.pk
                post.save()

                post_list = self.get_queryset_dict_list(
                    Post.objects.filter(id=post.id))
                return JsonResponse(post_list[0], safe=False)

            else:
                return JsonResponse(dict(form.errors.items()))
        elif 'delete' in request.POST.keys():
            Post.objects.get(id=request.POST['post_id']).delete()

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

    @staticmethod
    def get_meeting_list(queryset):
        meeting_query_list = queryset.values(
            'id',
            'title',
            'date',
            'description',
            'observation',
            'note_for_next_meeting', )
        meeting_list = []
        for meeting in meeting_query_list.iterator():
            meeting['date'] = datetime.strftime(meeting['date'], '%d.%m.%Y')
            meeting['images'] = []
            for image in MeetingImage.objects.filter(meeting_id=meeting['id']).iterator():
                meeting['images'].append(image.image.url)
            meeting_list.append(meeting)
        return meeting_list

    def get(self, request, *args, **kwargs):
        if 'get_meetings_data' in self.request.GET.keys():
            meeting_list = self.get_meeting_list(self.get_queryset())
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
        elif 'new_meeting' in self.request.POST.keys():
            instance = None
            if 'id' in self.request.POST.keys():
                instance = Meeting.objects.get(id=self.request.POST['id'])
            form = self.form_class(self.request.POST, instance=instance)
            if form.is_valid():
                meeting = form.save(commit=False)
                meeting.performer = Mentor.objects.get(pk=self.request.user.pk)
                meeting.save()
                for i in range(len(self.request.FILES)):
                    meeting_image = MeetingImage(meeting=meeting)
                    meeting_image.image.save(
                        self.request.FILES['new_image_{}'.format(i)].name,
                        self.request.FILES['new_image_{}'.format(i)])
                return JsonResponse(self.get_meeting_list(Meeting.objects.filter(id=meeting.id))[0])
            else:
                errors = dict(form.errors.items())
                errors['errors'] = True
                return JsonResponse(errors)

        return JsonResponse({'status': 'success'})


def like_news_item(request):
    post = Post.objects.get(id=request.POST['post_id'])
    if request.user.id in post.likes.all().values_list('user_id', flat=True):
        post.likes.remove(request.user.id)
    else:
        post.likes.add(request.user.id)
    return JsonResponse({'likes': post.likes.count()})


class MentorSettingsView(UpdateView):
    template_name = 'mentors/mentor_settings.html'
    form_class = MentorSettingsForm
    questionnaire_form = MentorQuestionnaireSettingsForm

    def get_object(self, queryset=None):
        return Mentor.objects.get(pk=self.request.user.id)

    def get(self, request, *args, **kwargs):
        if 'get_mentor_data' in request.GET.keys():
            mentor_data = model_to_dict(
                self.get_object(),
                fields=(
                    'first_name',
                    'last_name',
                    'phone_number',
                )
            )
            mentor_questionnaire_data = model_to_dict(
                self.get_object().questionnaire,
                fields=(
                    'date_of_birth',
                    'phone_number',
                    'email',
                    'actual_address',
                )
            )
            mentor_questionnaire_data['date_of_birth'] = \
                datetime.strftime(mentor_questionnaire_data['date_of_birth'], '%d.%m.%Y')
            mentor_data.update(mentor_questionnaire_data)
            return JsonResponse(mentor_data)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        mentor = form.save(commit=False)
        questionnaire_form = self.questionnaire_form(self.request.POST)
        if questionnaire_form.is_valid():
            if form.cleaned_data.get('password_new1'):
                mentor.user.set_password(form.cleaned_data.get('password_new1'))
            mentor.user.email = questionnaire_form.cleaned_data['email']
            questionnaire = questionnaire_form.save(commit=False)
            mentor_questionnaire_dict = {k: v for k, v
                                         in questionnaire.__dict__.items()
                                         if v is not None}

            mentor.questionnaire.__dict__.update({k: v for k, v in mentor_questionnaire_dict.items() if v})
            mentor.questionnaire.save()
            mentor.save()
        else:
            return JsonResponse(dict(questionnaire_form.errors.items()))

        return JsonResponse({'status': 'success'})

    def form_invalid(self, form):
        questionnaire_form = self.questionnaire_form(self.request.POST)
        if questionnaire_form.is_valid():
            return JsonResponse(dict(form.errors.items()))
        else:
            errors = dict(form.errors.items())
            errors.update(dict(questionnaire_form.errors.items()))
            return JsonResponse(errors)


class SscReportView(CreateView):
    form_class = SscReportForm

    def form_valid(self, form):
        ssc_report = form.save(commit=False)
        ssc_report.ssc_id = self.request.POST['selected_ssc']
        ssc_report.save()

        return JsonResponse({'status': 'success'})

    def form_invalid(self, form):
        return JsonResponse(dict(form.errors.items()))


class SscAssessView(UpdateView):
    form_class = SscAssessForm

    def get_object(self, queryset=None):
        ssc = Coordinator.objects.get(mentor__pk=self.request.user.pk).social_service_center
        try:
            return SocialServiceCenterAssessment.objects.get(
                ssc=ssc, mentor__pk=self.request.user.pk)
        except SocialServiceCenterAssessment.DoesNotExist:
            return None

    def form_valid(self, form):
        ssc = Coordinator.objects.get(mentor__pk=self.request.user.pk).social_service_center
        ssc_assessment = form.save(commit=False)
        ssc_assessment.ssc = ssc
        ssc_assessment.mentor = Mentor.objects.get(user__pk=self.request.user.pk)
        ssc_assessment.save()

        return JsonResponse({'status': 'success'})

    def form_invalid(self, form):
        return JsonResponse(dict(form.errors.items()))


class UsefulContactsView(ListView):
    template_name = 'mentors/contacts.html'
    queryset = SocialServiceCenter.objects.all()


class ProforientationView(FormView):
    template_name = 'mentors/proforientation.html'
    form_class = ProforientationForm

    def get_queryset(self):
        proforientations = Proforientation.objects.all().values(
            'id',
            'company_name',
            'profession_name',
            'address',
            'meeting_days',
            'business_description',
            'phone_number',
        )

        for p in proforientations:
            p['related_mentors'] = \
                list(Proforientation
                     .objects.get(id=p['id'])
                     .related_mentor.all()
                     .values_list('user_id', flat=True))
        return nest_queryset(8, list(proforientations))

    def get(self, request, *args, **kwargs):
        if 'get_careers' in request.GET.keys():
            return JsonResponse(self.get_queryset(), safe=False)
        return super().get(request, *args, **kwargs)


def get_notifications(request):
    if request.method == 'GET':
        notifications = []

        tip_of_the_day = model_to_dict(TipOfTheDay.get_current_tip(), fields=('content', 'id'))
        if tip_of_the_day:
            notifications.append({'tip_of_the_day': tip_of_the_day})
        return JsonResponse(notifications, safe=False)
    elif request.method == 'POST':
        tip_of_the_day = TipOfTheDay.objects.get(id=request.POST['notification_id'])
        tip_of_the_day.watched_by.add(request.user.id)
        return JsonResponse({'status': 'success'})
