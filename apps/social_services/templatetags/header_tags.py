from django import template

register = template.Library()


@register.simple_tag
def get_social_service(user):
    return user.socialservicecenter


@register.simple_tag
def get_public_service(user):
    return user.publicservice
