from django.core.validators import RegexValidator
from django.db import models


class MentorLicenceKey(models.Model):
    mentor = models.ForeignKey(to='users.Mentor', on_delete=models.CASCADE)
    key_validator = RegexValidator(r'[a-zA-z]{2}\d{3}[a-zA-z]{3}\d{2}')
    key = models.CharField(max_length=10, validators=[key_validator])
