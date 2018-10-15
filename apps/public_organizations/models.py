from django.db import models
from django.core.validators import RegexValidator


class PublicOrganizationMasterKey(models.Model):
    master_key_validator = RegexValidator(
        regex=r'^.{8,12}$')
    master_key = models.CharField(
        max_length=12,
        validators=[master_key_validator])
