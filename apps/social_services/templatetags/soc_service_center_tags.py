from django import template
from django.db.models.fields.files import FieldFile, ImageFieldFile

from users.models import SocialServiceCenter

register = template.Library()


@register.filter
def get_service_data(user, attr):
    try:
        service = SocialServiceCenter.objects.get(pk=user.pk)
        if isinstance(getattr(service, attr), ImageFieldFile) or isinstance(getattr(service, attr), FieldFile):
            try:
                return getattr(service, attr).url
            except ValueError as e:
                return ''
        return getattr(service, attr)
    except SocialServiceCenter.DoesNotExist:
        return ''
