from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import UserTypes
from .models import Mentor, Volunteer

User = get_user_model()


class SignUpStep0Form(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = ('first_name', 'middle_name', 'phone_number',)


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
            raise ValidationError({'password1': _("Passwords didn't match.")})
        validate_password(password1)
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.user_type = UserTypes.MENTOR
            user.save()
        return user


class SignUpStep3Form(forms.Form):
    pass


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'city',
            'mentoring_popularization',
            'master_classes_names',
            'profession_name',
            'profession_company_name',
            'profession_company_address',
            'financial_support',
            'another_assistance_ways_names',
        )
