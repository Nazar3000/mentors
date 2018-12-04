from django import forms

from users.models import Volunteer


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'city',
            'mentoring_popularization',
            'make_master_classes',
            'master_classes_names',
            'talk_about_profession',
            'profession_name',
            'profession_company_name',
            'profession_company_address',
            'financial_support',
            'another_assistance_ways',
            'another_assistance_ways_names',
        )
