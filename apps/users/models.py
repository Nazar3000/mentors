import uuid
from contextlib import suppress

import rstr
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .constants import UserTypes, MentorStatuses, PublicServiceStatuses


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise TypeError('Users must have an email address.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('user_type', 1)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 0)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # TODO: End up when docs/requirements received
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    email = models.EmailField(
        db_index=True,
        unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Is the user account currently active',
    )
    user_type = models.PositiveSmallIntegerField(
        choices=UserTypes.USER_TYPE_CHOICES)
    user_master_key = models.CharField(
        max_length=12,
        blank=True,
        default=''
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()


class GovernUser(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        primary_key=True)


class Mentor(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        primary_key=True)
    status = models.CharField(
        max_length=64,
        choices=MentorStatuses.choices(),
        default=MentorStatuses.NOT_SPECIFIED
    )
    first_name = models.CharField(
        max_length=32)
    last_name = models.CharField(
        max_length=32)
    date_of_birth = models.DateField(blank=True, null=True)
    actual_address = models.CharField(
        max_length=521
    )
    questionnaire_creation_date = models.DateField(blank=True, null=True)

    phone_regex = RegexValidator(
        regex=r'\+?1?\d$')
    phone_number = models.CharField(
        max_length=17,
        validators=[phone_regex])
    mentoree = models.OneToOneField(
        to='mentors.Mentoree',
        on_delete=models.SET_NULL,
        null=True)
    licence_key = models.OneToOneField(
        to='mentors.MentorLicenceKey',
        on_delete=models.SET_NULL,
        null=True)
    profile_image = models.ImageField(
        upload_to='mentors/profile_images')
    licenced = models.BooleanField(
        default=False
    )
    coordinator = models.ForeignKey(
        to='users.Coordinator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mentors'
    )

    base_social_service_center = models.ForeignKey(
        to='social_services.BaseSocialServiceCenter',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )


class SocialServiceCenter(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        primary_key=True)

    name = models.CharField(
        max_length=256
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


class SocialServiceCenterReport(models.Model):
    ssc = models.ForeignKey(
        to=SocialServiceCenter,
        on_delete=models.CASCADE
    )
    content = models.TextField()


class SocialServiceCenterAssessment(models.Model):
    ssc = models.ForeignKey(
        to=SocialServiceCenter,
        on_delete=models.CASCADE
    )
    mentor = models.OneToOneField(
        to=Mentor,
        on_delete=models.CASCADE
    )
    grade = models.PositiveSmallIntegerField(
        default=0,
        validators=[MaxValueValidator(5)]
    )
    mentor_help_description = models.TextField(
        null=True,
        blank=True
    )
    mentor_pair_help_description = models.TextField(
        null=True,
        blank=True
    )


class PublicService(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        primary_key=True)
    social_service_center = models.ForeignKey(
        to=SocialServiceCenter,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=128
    )
    profile_image = models.ImageField(
        upload_to='public_services/profile_images',
        null=True,
        blank=True)
    max_pair_count = models.PositiveSmallIntegerField(
        default=1
    )
    phone_regex = RegexValidator(
        regex=r'\+?1?\d$')
    phone_number = models.CharField(
        max_length=17,
        validators=[phone_regex])
    email = models.EmailField()
    address = models.CharField(
        max_length=512
    )
    website = models.URLField()
    status = models.CharField(
        max_length=64,
        choices=PublicServiceStatuses.choices(),
        default=PublicServiceStatuses.NOT_SPECIFIED.name
    )
    contract_number = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    licence_validator = RegexValidator(
        regex=r'[A-Z]{4}\s{1}\d{2}')
    licence = models.CharField(
        max_length=7,
        validators=[licence_validator],
        blank=True)

    @property
    def pair_count(self):
        pair_count = 0
        for c in self.coordinators.all().iterator():
            pair_count += c.mentors.count()
        return pair_count

    def save(self, *args, **kwargs):
        if not self.licence:
            self.licence = rstr.xeger(self.licence_validator.regex)
        super().save(*args, **kwargs)


class Organization(models.Model):
    name = models.CharField(
        max_length=512)
    address = models.CharField(
        max_length=512)
    phone_regex = RegexValidator(
        regex=r'\+?1?\d$')
    phone_numbers = ArrayField(
        models.CharField(
            max_length=17,
            validators=[phone_regex]
        )
    )


class ChildService(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    pass


class Volunteer(models.Model):
    first_name = models.CharField(
        max_length=32)
    last_name = models.CharField(
        max_length=32)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=64)

    city = models.CharField(
        max_length=64)

    mentoring_popularization = models.BooleanField(
        default=True)

    make_master_classes = models.BooleanField(
        default=True
    )
    master_classes_names = models.CharField(
        max_length=512,
        blank=True,
        null=True)

    talk_about_profession = models.BooleanField(
        default=True
    )
    profession_name = models.CharField(
        max_length=128,
        blank=True,
        null=True)
    profession_company_name = models.CharField(
        max_length=128,
        blank=True,
        null=True)
    profession_company_address = models.CharField(
        max_length=256,
        blank=True,
        null=True)

    financial_support = models.BooleanField(
        default=True)

    another_assistance_ways = models.BooleanField(
        default=True
    )
    another_assistance_ways_names = models.CharField(
        max_length=512,
        blank=True,
        null=True)


class Coordinator(models.Model):
    image = models.ImageField(
        upload_to='mentorees/coordinator_images',
        null=True,
        blank=True
    )
    full_name = models.CharField(
        max_length=256,

    )
    phone_regex = RegexValidator(
        regex=r'\+?1?\d$')
    phone_numbers = ArrayField(
        models.CharField(
            max_length=17,
            validators=[phone_regex]
        )
    )
    email = models.EmailField()

    # One of social_service_center or public_service need to be filled
    # but one of them should be null
    social_service_center = models.ForeignKey(
        to='users.SocialServiceCenter',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='coordinators'
    )
    public_service = models.ForeignKey(
        to='users.PublicService',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='coordinators'
    )

    @classmethod
    def get_coordinator_by_related_service_pk(cls, service_pk):
        try:
            coordinator = SocialServiceCenter.objects.get(pk=service_pk).coordinators.first()
        except SocialServiceCenter.DoesNotExist:
            coordinator = PublicService.objects.get(pk=service_pk).coordinators.first()
        except PublicService.DoesNotExist:
            raise Coordinator.DoesNotExist

        return coordinator


class UsefulContact(models.Model):
    name = models.CharField(max_length=256)
    logo = models.ImageField(upload_to='useful_contacts')
    description = models.TextField()
    phone_regex = RegexValidator(
        regex=r'\+?1?\d$')
    phone_number = models.CharField(
        max_length=17,
        validators=[phone_regex])
    email = models.EmailField()
    address = models.CharField(max_length=4096)
