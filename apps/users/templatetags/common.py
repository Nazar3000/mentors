from django import template

from users.models import Mentor, MentoreesCount

register = template.Library()


@register.simple_tag
def get_mentors_count_str():
    count = str(Mentor.objects.filter(licenced=True).count())
    return count.zfill(4)


@register.simple_tag
def mentorees_count():
    return MentoreesCount.objects.first().count if MentoreesCount.objects.first() else 0
