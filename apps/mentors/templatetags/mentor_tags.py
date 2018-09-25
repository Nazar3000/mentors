from django import template
from django.db.models.fields.files import ImageFieldFile, FieldFile

from users.models import Mentor, SocialServiceCenter, Coordinator

register = template.Library()


@register.filter
def get_mentor_data(user, attr):
    mentor = Mentor.objects.get(pk=user.pk)
    if isinstance(getattr(mentor, attr), ImageFieldFile) or isinstance(getattr(mentor, attr), FieldFile):
        try:
            return getattr(mentor, attr).url
        except ValueError as e:
            return ''
    return getattr(mentor, attr)


@register.simple_tag
def get_social_service_centers():
    return SocialServiceCenter.objects.all().values('pk', 'name')


@register.simple_tag
def get_related_coordinator(user):
    if Coordinator.objects.filter(mentor__pk=user.id).exists():
        return Coordinator.objects.get(mentor__pk=user.id)


@register.simple_tag
def get_useful_contacts():
    return 