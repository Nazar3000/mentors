from django.core.validators import RegexValidator
from django.db import models


class MentorLicenceKey(models.Model):
    mentor = models.ForeignKey(to='users.Mentor', on_delete=models.CASCADE)
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
    extra_data = models.CharField(max_length=128)
    organization = models.OneToOneField(
        to='users.Organization',
        on_delete=models.SET_NULL,
        null=True)
    address = models.CharField(max_length=128)
    profile_image = models.ImageField(upload_to='mentorees/profile_images')

    hygiene = models.CharField(max_length=64)
    will_help_to_became_independent = models.CharField(max_length=64)
    emotional_state = models.CharField(max_length=64)
    communication_skills = models.CharField(max_length=64)
    how_orients_in_environment = models.CharField(max_length=64)

    story = models.TextField()


class StoryImage(models.Model):
    # TODO: find out how many images should be available to upload
    mentoree = models.ForeignKey(to=Mentoree, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='mentorees/story_images')


class Meeting(models.Model):
    title = models.CharField(max_length=16)
    date = models.DateField()
    description = models.TextField()
    observation = models.TextField()
    note_for_next_meeting = models.TextField()


class MeetingImage(models.Model):
    # TODO: find out how many images should be available to upload
    meeting = models.ForeignKey(to=Meeting, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='mentorees/meeting_images')
