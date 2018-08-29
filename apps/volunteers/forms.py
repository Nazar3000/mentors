from django import forms

from users.models import Volunteer


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
