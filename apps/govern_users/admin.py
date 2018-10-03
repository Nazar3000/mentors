from django.contrib import admin

from .models import MentorSchoolVideo, MentorSchoolVideoExtraMaterial, MentorTip, TipOfTheDay

admin.site.register(MentorSchoolVideo)
admin.site.register(MentorSchoolVideoExtraMaterial)
admin.site.register(MentorTip)
admin.site.register(TipOfTheDay)
