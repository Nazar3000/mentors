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


class BaseSocialServiceCenterManager(models.Manager):
    def unlinked(self):
        queryset = super().get_queryset()
        return queryset.filter(service__isnull=True)


class BaseSocialServiceCenter(models.Model):
    """
    Non user SocialServiceCenter data. Fill it by fixtures.
    """
    name = models.CharField(
        max_length=2014
    )
    region = models.CharField(
        max_length=64,
        null=True,
        blank=True
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

    service = models.OneToOneField(
        to='users.SocialServiceCenter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    objects = BaseSocialServiceCenterManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__old_service = self.service

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.__old_service != self.service and self.service is not None:
            coordinator = self.service.coordinators.first()
            for mentor in self.mentor_set.all():
                mentor.coordinator = coordinator
                mentor.save()


class Question(models.Model):
    social_service_center = models.ForeignKey(
        to='users.SocialServiceCenter',
        on_delete=models.CASCADE
    )
    body = models.TextField()
