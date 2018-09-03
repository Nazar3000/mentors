from datetime import datetime

from dateutil.relativedelta import relativedelta
from django import template

register = template.Library()


@register.filter
def get_age(date_of_birth):
    """
    Returns age from a provided date of birth
    """
    return (datetime.now().date() - relativedelta(years=date_of_birth.year)).year
