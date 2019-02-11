from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import (
    GovernUser,
    Mentor,
    SocialServiceCenter,
    PublicService,
    Organization,
    ChildService,
    Volunteer,
    Coordinator,
    SocialServiceCenterReport,
    SocialServiceCenterAssessment,
    MentoreesCount)

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('email',)


@admin.register(GovernUser)
class GovernUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    search_fields = ('user__email',)


@admin.register(SocialServiceCenter)
class SocialServiceCenterAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(PublicService)
class PublicServiceAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(ChildService)
class ChildServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    pass


@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)


@admin.register(SocialServiceCenterReport)
class SocialServiceCenterReportAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialServiceCenterAssessment)
class SocialServiceCenterAssessmentAdmin(admin.ModelAdmin):
    pass


@admin.register(MentoreesCount)
class MentoreesCountAdmin(admin.ModelAdmin):
    pass
