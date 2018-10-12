from django import forms

from users.models import Mentor


class MentorEditForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = (
            'status',
            'first_name',
            'last_name',
            'phone_number',
            'profile_image',
        )
