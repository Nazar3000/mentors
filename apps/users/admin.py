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
)

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


# admin.site.register(User)
admin.site.register(GovernUser)
admin.site.register(Mentor)
admin.site.register(SocialServiceCenter)
admin.site.register(PublicService)
admin.site.register(Organization)
admin.site.register(ChildService)
admin.site.register(Volunteer)
