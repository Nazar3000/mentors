from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import RegexValidator


class SocialServiceMasterKey(models.Model):
    master_key_validator = RegexValidator(
        regex=r'^.{8,12}$')
    master_key = models.CharField(
        max_length=12,
        validators=[master_key_validator])


class SocialServiceVideo(models.Model):

    PAGE_CHOICES = ((1, 'Main'),
                    (2, 'Video Mentor'),
                    )

    video_link = models.URLField()
    page = models.IntegerField(choices=PAGE_CHOICES)


class MaterialCategory(models.Model):
    title = models.CharField(max_length=256)
    icon = models.ImageField(upload_to='icons', blank=True, null=True)

    class Meta:
        verbose_name = "Material category"
        verbose_name_plural = "Material categories"

    def __str__(self):
        return "{}".format(self.title)


class Material(models.Model):
    title = models.CharField(max_length=256)
    file = models.FileField(blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    category = models.ForeignKey(MaterialCategory, blank=True, null=True, on_delete=models.SET_NULL)


class BaseSocialServiceCenter(models.Model):
    """
    Non user SocialServiceCenter data. Fill it by fixtures.
    """
    name = models.CharField(
        max_length=256
    )
    region = models.CharField(
        max_length=64
    )
    city = models.CharField(
        max_length=256
    )
    address = models.CharField(
        max_length=512
    )
    phone_numbers = ArrayField(
        models.CharField(
            max_length=128
        )
    )
