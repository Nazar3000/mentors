from social_services.forms import AuthenticationForm
from django.core.exceptions import ValidationError


class SPAuthenticationForm(AuthenticationForm):

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if email != 'msp@sample.com':
            raise ValidationError('Користувач з цією електронною адресою не зареєстрований.')
        return email



