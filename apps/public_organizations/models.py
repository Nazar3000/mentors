from django.db import models
from django.core.validators import RegexValidator


class PublicOrganizationMasterKey(models.Model):
    master_key_validator = RegexValidator(
        regex=r'^.{8,12}$')
    master_key = models.CharField(
        max_length=12,
        validators=[master_key_validator])


class PublicOrganizationVideo(models.Model):

    PAGE_CHOICES = ((1, 'Main'),
                    (2, 'Video Mentor'),
                    )

    video_link = models.URLField()
    page = models.IntegerField(choices=PAGE_CHOICES)

