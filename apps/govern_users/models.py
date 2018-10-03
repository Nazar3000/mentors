import datetime

from dateutil.tz import tzlocal
from django.core.exceptions import ValidationError
from django.db import models


class MentorSchoolVideo(models.Model):
    """
    Specify either video or video_url
    """
    title = models.CharField(
        max_length=32)
    video = models.FileField(
        upload_to='govern_users/mentor_school_videos',
        null=True,
        blank=True)
    thumbnail = models.ImageField(
        upload_to='govern_users/mentor_school_videos/thumbnails')
    video_url = models.URLField(
        null=True,
        blank=True)
    watched_by = models.ManyToManyField(
        to='users.Mentor',
        blank=True)

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
    file = models.FileField(
        upload_to='govern_users/mentor_school_videos/extra_materials')


class MentorTip(models.Model):
    title = models.CharField(
        max_length=32)
    content = models.TextField()
    image = models.ImageField(
        upload_to='govern_users/mentor_tips')


class TipOfTheDay(models.Model):
    content = models.CharField(
        max_length=256
    )
    last_swap_date = models.DateTimeField(
        auto_now=True
    )
    watched_by = models.ManyToManyField(
        to='users.Mentor'
    )

    @staticmethod
    def get_current_tip():
        if TipOfTheDay.objects.count():
            current_tip = TipOfTheDay.objects.latest('last_swap_date')
            if (datetime.datetime.utcnow() - current_tip.last_swap_date.replace(tzinfo=None)).days >= 1:
                for tip in TipOfTheDay.objects.iterator():
                    if tip == current_tip:
                        current_tip = next(TipOfTheDay.objects.iterator())
                        break
            return current_tip
        return None
