from django import template

from users.models import PublicService

register = template.Library()


@register.simple_tag
def get_social_service(user):
    return user.socialservicecenter


@register.simple_tag
def get_public_service(user):
    try:
        return PublicService.objects.get(user=user)
    except:
        return ''
