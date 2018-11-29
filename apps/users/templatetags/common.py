from django import template

from users.models import Mentor

register = template.Library()


@register.simple_tag
def get_mentors_count_str():
    count = str(Mentor.objects.filter(licenced=True).count())
    return count.zfill(4)
