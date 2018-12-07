from django.contrib import admin

from .models import (
    MentorLicenceKey,
    Mentoree,
    StoryImage,
    Meeting,
    MeetingImage,
    Post,
    PostComment,
    MentorQuestionnaire,
    MentorQuestionnaireEducation,
    MentorQuestionnaireJob,
    MentorQuestionnaireFamilyMember,
    MentorQuestionnaireChildrenWorkExperience,
    Proforientation,
    MentorSocialServiceCenterData,
    RoadmapDoc)


@admin.register(MentorLicenceKey)
class MentorLicenceKeyAdmin(admin.ModelAdmin):
    pass


@admin.register(Mentoree)
class MentoreeAdmin(admin.ModelAdmin):
    pass


@admin.register(StoryImage)
class StoryImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    pass


@admin.register(MeetingImage)
class MeetingImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(MentorQuestionnaire)
class MentorQuestionnaireAdmin(admin.ModelAdmin):
    pass


@admin.register(MentorQuestionnaireEducation)
class MentorQuestionnaireEducationAdmin(admin.ModelAdmin):
    pass


@admin.register(MentorQuestionnaireJob)
class MentorQuestionnaireJobAdmin(admin.ModelAdmin):
    pass


@admin.register(MentorQuestionnaireFamilyMember)
class MentorQuestionnaireFamilyMemberAdmin(admin.ModelAdmin):
    pass


@admin.register(MentorQuestionnaireChildrenWorkExperience)
class MentorQuestionnaireChildrenWorkExperienceAdmin(admin.ModelAdmin):
    pass


@admin.register(Proforientation)
class ProforientationAdmin(admin.ModelAdmin):
    pass


@admin.register(MentorSocialServiceCenterData)
class MentorSocialServiceCenterDataAdmin(admin.ModelAdmin):
    pass


@admin.register(RoadmapDoc)
class RoadmapDocAdmin(admin.ModelAdmin):
    pass
