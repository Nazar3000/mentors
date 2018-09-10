from django import template
from django.db.models.fields.files import ImageFieldFile, FieldFile

from users.models import Mentor

register = template.Library()


@register.filter
def get_mentor_data(user, attr):
    mentor = Mentor.objects.get(pk=user.pk)
    if isinstance(getattr(mentor, attr), ImageFieldFile) or isinstance(getattr(mentor, attr), FieldFile):
        return getattr(mentor, attr).url
    return getattr(mentor, attr)
