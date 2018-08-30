from django.contrib import admin

from .models import (
    MentorLicenceKey,
    Mentoree,
    StoryImage,
    Meeting,
    MeetingImage,
    Post,
    PostComment)

admin.site.register(MentorLicenceKey)
admin.site.register(Mentoree)
admin.site.register(StoryImage)
admin.site.register(Meeting)
admin.site.register(MeetingImage)
admin.site.register(Post)
admin.site.register(PostComment)
