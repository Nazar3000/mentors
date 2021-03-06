from datetime import datetime

from dateutil.relativedelta import relativedelta
from dateutil.tz import tzlocal
from django import template

register = template.Library()


@register.filter
def get_age(date_of_birth):
    """
    Return age from a provided date of birth.
    """
    try:
        return (datetime.now().date() - relativedelta(years=date_of_birth.year)).year
    except (TypeError, AttributeError, ValueError):
        return 0


@register.filter
def get_time_spent(datetime_value):
    """
    Return time spent value if it was spent less then 24 hours,
    otherwise return datetime_value.
    """
    try:
        time_delta = datetime.now(tzlocal()) - datetime_value
        time_delta_seconds = time_delta.seconds
        if time_delta.days < 1:
            if time_delta_seconds < 60:
                return '{} сек тому'.format(time_delta_seconds)
            elif 60 <= time_delta_seconds < 60 * 60:
                return '{} хв тому'.format(time_delta_seconds // 60)
            elif 60 * 60 <= time_delta_seconds < 60 * 60 * 24:
                return '{} год тому'.format(time_delta_seconds // (60 * 60))
        else:
            return datetime_value.strftime('%d.%m.%Y')
    except (TypeError, AttributeError):
        return ''
