from django.core.exceptions import ValidationError
from django.db import models


class MentorSchoolVideo(models.Model):
    """
    Specify either video or video_url
    """
    title = models.CharField(max_length=32)
    video = models.FileField(
        upload_to='govern_users/mentor_school_videos',
        null=True,
        blank=True)
    thumbnail = models.ImageField(upload_to='govern_users/mentor_school_videos/thumbnails')
    video_url = models.URLField(null=True, blank=True)
    watched_by = models.ManyToManyField(to='users.Mentor', blank=True)

    def clean(self):
        if not self.video and not self.video_url:
            raise ValidationError('Одне з полів має бути заповненим: video, video_url')
        elif self.video and self.video_url:
            raise ValidationError('Заповніть тільки одне з полів: video, video_url')


class MentorSchoolVideoExtraMaterial(models.Model):
    video = models.ForeignKey(
        to=MentorSchoolVideo,
        on_delete=models.CASCADE,
        related_name='extra_materials')
    file = models.FileField('govern_users/mentor_school_videos/extra_materials')


class MentorTip(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()
    image = models.ImageField('govern_users/mentor_tips')
