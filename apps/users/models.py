import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import UserTypes


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
    user_type = models.PositiveSmallIntegerField(
        choices=UserTypes.USER_TYPE_CHOICES)

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
    first_name = models.CharField(
        max_length=32)
    last_name = models.CharField(
        max_length=32)

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


class SocialServiceCenter(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        primary_key=True)
    mentor_license_key = models.ForeignKey(
        to='mentors.MentorLicenceKey',
        on_delete=models.SET_NULL,
        null=True)


class PublicService(models.Model):
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        primary_key=True)


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
            validators=[phone_regex]))


class ChildService(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    pass


class Volunteer(models.Model):
    first_name = models.CharField(
        max_length=32)
    last_name = models.CharField(
        max_length=32)

    phone_regex = RegexValidator(
        regex=r'\+?1?\d$')
    phone_number = models.CharField(
        max_length=17,
        validators=[phone_regex])

    city = models.CharField(
        max_length=64)

    mentoring_popularization = models.BooleanField(
        default=True)

    master_classes_names = models.CharField(
        max_length=512)

    profession_name = models.CharField(
        max_length=128)
    profession_company_name = models.CharField(
        max_length=128)
    profession_company_address = models.CharField(
        max_length=256)

    financial_support = models.BooleanField(
        default=True)

    another_assistance_ways_names = models.CharField(
        max_length=512)
