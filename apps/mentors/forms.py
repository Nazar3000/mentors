from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Meeting, MeetingImage, MentorQuestionnaire, MentorQuestionnaireEducation, \
    MentorQuestionnaireJob, MentorQuestionnaireFamilyMember, MentorQuestionnaireChildrenWorkExperience, Mentoree, Post, \
    Proforientation
from users.constants import UserTypes
from users.models import Mentor, SocialServiceCenterReport, SocialServiceCenterAssessment

User = get_user_model()


class SignUpStep0Form(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Mentor
        fields = ('first_name', 'last_name', 'phone_number',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Користувач з цією електронною адресою вже зареєстрований.')
        return email


class SignUpStep1Form(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']
        if password1 != password2:
            raise ValidationError({'password1': 'Паролі не співпадають.'})
        validate_password(password1)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.user_type = UserTypes.MENTOR
            user.save()
        return user


class MentorQuestionnaireForm(forms.ModelForm):
    class Meta:
        model = MentorQuestionnaire
        exclude = (
            'mentor',
        )


class MentorQuestionnaireEducationForm(forms.ModelForm):
    class Meta:
        model = MentorQuestionnaireEducation
        exclude = (
            'questionnaire',
        )


class MentorQuestionnaireJobForm(forms.ModelForm):
    class Meta:
        model = MentorQuestionnaireJob
        exclude = (
            'questionnaire',
        )


class MentorQuestionnaireFamilyMemberForm(forms.ModelForm):
    class Meta:
        model = MentorQuestionnaireFamilyMember
        exclude = (
            'questionnaire',
        )


class MentorQuestionnaireChildrenWorkExperienceForm(forms.ModelForm):
    class Meta:
        model = MentorQuestionnaireChildrenWorkExperience
        exclude = (
            'questionnaire',
        )


class SignUpStep2Forms:
    forms = {
        'main': MentorQuestionnaireForm,
        'education': MentorQuestionnaireEducationForm,
        'job': MentorQuestionnaireJobForm,
        'family_member': MentorQuestionnaireFamilyMemberForm,
        'children_work_experience': MentorQuestionnaireChildrenWorkExperienceForm,
    }


class MeetingForm(forms.ModelForm):
    date = forms.DateField(error_messages={
        'invalid': _('Введіть дату у форматі дд.мм.рррр')})

    class Meta:
        model = Meeting
        fields = (
            'title',
            'date',
            'description',
            'observation',
            'note_for_next_meeting',
        )


class MeetingImageForm(forms.ModelForm):
    class Meta:
        model = MeetingImage
        fields = ('image',)


class MentoreeEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=['%d.%m.%Y'], required=False)

    class Meta:
        model = Mentoree
        fields = (
            'first_name',
            'last_name',
            'date_of_birth',
            'dream',
            'want_to_become',
            'fears',
            'loves',
            'hates',
            'strengths',
            'extra_data',
            'profile_image',
        )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'content',
            'image'
        )


class MentorQuestionnaireSettingsForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=['%d.%m.%Y'])
    full_name = forms.CharField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()

    def clean_full_name(self):
        print(self.cleaned_data)
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        self.cleaned_data['full_name'] = '{} {}'.format(first_name, last_name)

    class Meta:
        model = MentorQuestionnaire
        fields = (
            'email',
        )


class MentorSettingsForm(forms.ModelForm):
    email = forms.EmailField()
    password_old = forms.CharField(required=False)
    password_new1 = forms.CharField(required=False)
    password_new2 = forms.CharField(required=False)

    class Meta:
        model = Mentor
        fields = (
            'first_name',
            'last_name',
            'phone_number',
        )

    def clean_password_old(self):
        password_old = self.cleaned_data.get('password_old')
        if password_old and not self.instance.user.check_password(password_old):
            raise ValidationError(_('Неправильний пароль.'))

    def clean(self):
        password_new1 = self.cleaned_data.get('password_new1')
        password_new2 = self.cleaned_data.get('password_new2')

        if password_new1 or password_new2:
            validate_password(password_new1)

            if password_new1 != password_new2:
                raise ValidationError({'password_new1': _('Паролі не співпадають.')})


class SscReportForm(forms.ModelForm):
    class Meta:
        model = SocialServiceCenterReport
        fields = (
            'content',
        )


class SscAssessForm(forms.ModelForm):
    class Meta:
        model = SocialServiceCenterAssessment
        fields = (
            'grade',
            'mentor_help_description',
            'mentor_pair_help_description',
        )


class ProforientationForm(forms.ModelForm):
    class Meta:
        model = Proforientation
        fields = (
            'company_name',
            'profession_name',
            'address',
            'meeting_days',
            'business_description',
            'phone_number',
        )
