from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from users.constants import UserTypes
from users.models import PublicService
from .models import PublicServiceMasterKey, Question
from social_services.forms import SignUpStep0Form
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class PublicServiceSignUpStep0Form(SignUpStep0Form):

    def clean_master_key(self):
        master_key = self.cleaned_data['master_key']
        if not PublicServiceMasterKey.objects.filter(master_key=master_key).exists():
            raise ValidationError('Невірний ключ.')
        return master_key

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        master_key = self.cleaned_data['master_key']
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.user_type = UserTypes.PUBLIC_SERVICE
            user.user_master_key = master_key
            user.save()
        return user


class PublicServiceForm(forms.ModelForm):
    class Meta:
        model = PublicService
        fields = (
            'name',
            'phone_number',
            'address',
            'website',
            'contract_number',
        )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = (
            'body',
        )
