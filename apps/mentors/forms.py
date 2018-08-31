from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from users.constants import UserTypes
from users.models import Mentor

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


class SignUpStep3Form(forms.Form):
    pass
