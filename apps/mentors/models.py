from django.contrib.postgres.fields import HStoreField
from django.core.validators import RegexValidator
from django.db import models

from .constants import Regions


class MentorLicenceKey(models.Model):
    key_validator = RegexValidator(r'[a-zA-z]{2}\d{3}[a-zA-z]{3}\d{2}')
    key = models.CharField(max_length=10, validators=[key_validator])


class Mentoree(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField()
    dream = models.CharField(max_length=128)
    want_to_become = models.CharField(max_length=32)
    fears = models.CharField(max_length=128)
    loves = models.CharField(max_length=64)
    hates = models.CharField(max_length=64)
    strengths = models.CharField(max_length=64)
    extra_data = models.CharField(max_length=128)
    organization = models.OneToOneField(
        to='users.Organization',
        on_delete=models.SET_NULL,
        null=True)
    address = models.CharField(max_length=128)
    profile_image = models.ImageField(upload_to='mentorees/profile')
    extra_data_fields = HStoreField(default=dict)

    story = models.TextField()


class StoryImage(models.Model):
    # TODO: find out how many images should be available to upload
    mentoree = models.ForeignKey(to=Mentoree, on_delete=models.CASCADE, related_name='story_images')
    image = models.ImageField(upload_to='mentorees/story')


class Meeting(models.Model):
    performer = models.ForeignKey(
        to='users.Mentor',
        on_delete=models.CASCADE,
        related_name='meetings')
    title = models.CharField(max_length=16)
    date = models.DateField()
    description = models.TextField()
    observation = models.TextField()
    note_for_next_meeting = models.TextField()


class MeetingImage(models.Model):
    # TODO: find out how many images should be available to upload
    meeting = models.ForeignKey(to=Meeting, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='mentorees/meeting')


class Post(models.Model):
    author = models.ForeignKey(to='users.Mentor', on_delete=models.CASCADE)
    related_user = models.ForeignKey(
        to='users.Mentor',
        on_delete=models.CASCADE,
        related_name='posts')
    content = models.TextField()
    region = models.CharField(max_length=16, choices=Regions.choices())
    image = models.ImageField(upload_to='mentorees/post')
    likes = models.PositiveSmallIntegerField(default=0)
    datetime = models.DateTimeField(auto_now=True)


class PostComment(models.Model):
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    datetime = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to='users.Mentor', on_delete=models.CASCADE)
    content = models.TextField()
