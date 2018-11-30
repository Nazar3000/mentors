from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from users.constants import UserTypes
from .models import SocialServiceMasterKey, BaseSocialServiceCenter
from mentors.models import MentorSocialServiceCenterData
from users.models import Mentor, PublicService, SocialServiceCenter, Coordinator

User = get_user_model()


class SignUpStep0Form(UserCreationForm):
    master_key = forms.CharField()

    class Meta:
        model = User
        fields = ('email', 'master_key',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(_('Користувач з цією електронною адресою вже зареєстрований.'))
        return email

    def clean_master_key(self):
        master_key = self.cleaned_data['master_key']
        if not SocialServiceMasterKey.objects.filter(master_key=master_key).exists():
            raise ValidationError('Невірний ключ.')
        return master_key

    def save(self, commit=True):
        user = super().save(commit=False)
        master_key = self.cleaned_data['master_key']
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.user_type = UserTypes.SOCIAL_SERVICE_CENTER
            user.user_master_key = master_key
            user.save()
        return user


class AuthenticationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ('email', 'password')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if not User.objects.filter(email=email).exists():
            raise ValidationError(_('Користувач з цією електронною адресою не зареєстрований.'))
        return email


class MentorEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=['%d.%m.%Y'])
    email = forms.EmailField()

    class Meta:
        model = Mentor
        fields = (
            'status',
            'first_name',
            'last_name',
            'phone_number',
            'profile_image',
            'date_of_birth',
            'actual_address',
        )


class MentorSocialServiceCenterDataEditForm(forms.ModelForm):
    passport_copy = forms.BooleanField(widget=forms.CheckboxInput, initial=False, required=False)
    application = forms.BooleanField(widget=forms.CheckboxInput, initial=False, required=False)
    certificate_of_good_conduct = forms.BooleanField(widget=forms.CheckboxInput, initial=False, required=False)
    medical_certificate = forms.BooleanField(widget=forms.CheckboxInput, initial=False, required=False)
    recommended_to_training = forms.BooleanField(widget=forms.CheckboxInput, initial=False, required=False)
    admitted_to_child = forms.BooleanField(widget=forms.CheckboxInput, initial=False, required=False)

    class Meta:
        model = MentorSocialServiceCenterData
        exclude = (
            'mentor',
        )


class PublicServiceEditForm(forms.ModelForm):
    class Meta:
        model = PublicService
        fields = (
            'name',
            'max_pair_count',
            'phone_number',
            'email',
            'address',
            'website',
            'contract_number',
            'profile_image',
        )


class DatingSocialServiceCenterForm(forms.ModelForm):
    class Meta:
        model = SocialServiceCenter
        fields = (
            'name',
            'city',
            'address',
            'phone_numbers',
        )


class DatingBaseSocialServiceCenterForm(forms.ModelForm):
    class Meta:
        model = BaseSocialServiceCenter
        fields = (
            'name',
            'city',
            'address',
            'phone_numbers',
        )


class DatingCoordinatorForm(forms.ModelForm):
    class Meta:
        model = Coordinator
        fields = (
            'full_name',
            'phone_numbers',
            'email',
        )
