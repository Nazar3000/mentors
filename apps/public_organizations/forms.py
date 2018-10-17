from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from users.constants import UserTypes
from .models import PublicOrganizationMasterKey
from social_services.forms import SignUpStep0Form

User = get_user_model()


class PublicOrganizationSignUpStep0Form(SignUpStep0Form):

    def clean_master_key(self):
        master_key = self.cleaned_data['master_key']
        if not PublicOrganizationMasterKey.objects.filter(master_key=master_key).exists():
            raise ValidationError('Невірний ключ.')
        PublicOrganizationMasterKey.objects.filter(master_key=master_key).first().delete()
        return master_key

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.user_type = UserTypes.PUBLIC_SERVICE
            user.save()
        return user




