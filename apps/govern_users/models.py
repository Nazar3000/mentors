from django.db import models


class MentorSchoolVideo(models.Model):
    title = models.CharField(max_length=32)
    video = models.FileField(upload_to='govern_users/mentor_school_videos')
    watched_by = models.ManyToManyField(to='users.Mentor')


class MentorSchoolVideoExtraMaterial(models.Model):
    video = models.ForeignKey(to=MentorSchoolVideo, on_delete=models.CASCADE)
    file = models.FileField('govern_users/mentor_school_videos/extra_materials')


class MentorTip(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()
