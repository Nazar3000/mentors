import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


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
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # TODO: End up when docs/requirements received
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(db_index=True, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()


class GovernUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class SocialServiceCenter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class PublicService(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class Institution(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class ChildService(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


class ProjectAssistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
