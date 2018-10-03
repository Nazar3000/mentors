from django.utils.translation import gettext_lazy as _

from users.constants import ChoicesEnum


class Religions(ChoicesEnum):
    CHRISTIANITY = _('Християнство')
    CATHOLICISM = _('Католицизм')
    ORTHODOXY = _('Православ’я')
    PROTESTANTISM = _('Протестантизм')
    JUDAISM = _('Іудаїзм')
    BUDDHISM = _('Буддизм')
    ISLAM = _('Іслам')
    OTHER = _('Інше')


class LocalChurchVisitingFrequency(ChoicesEnum):
    ONCE_A_WEEK = _('раз на тиждень')
    ONCE_A_MONTH = _('раз на місяць')
    ONCE_A_YEAR = _('один раз на рік')
    OTHER = _('інше')


class MaritalStatuses(ChoicesEnum):
    MARRIED = _('Одружений/одружена')
    CIVIL_MARRIAGE = _('Цивільний шлюб')
    DIVORCED = _('Розлучений/розлучена')
    WIDOW = _('Удовець/удова')
    UNMARRIED = _('Неодружений/неодружена')


class Genders(ChoicesEnum):
    MALE = _('чоловіча')
    FEMALE = _('жіноча')


class HomeTypes(ChoicesEnum):
    APARTMENT = _('квартира')
    PRIVATE_HOUSE = _('приватний будинок')
    RENTED = _('орендоване житло')


class AbleToVisitChildFrequency(ChoicesEnum):
    ONCE_A_WEEK = _('1 раз на тиждень')
    ONCE_A_TWO_WEEKS = _('1 раз на 2 тижні')
    ONCE_A_MONTH = _('1 раз на місяць')
    OTHER = _('інше')


class MentoringProgramFindOutPlaces(ChoicesEnum):
    TV = _('Телебачення')
    RADIO = _('Радіо')
    OTHER_MEDIA = _('Інші ЗМІ')
    FACEBOOK_OR_OTHER_SOCIAL_NETWORKS = _('Facebook або інші соціальні мережі')
    INTERNET = _('Інтернет')
    FRIENDS_RELATIVES_ACQUAINTANCES = _('Друзі, рідні, знайомі')
    PAPERS = _('Друковані матеріали')
    PRESENTATION_CONFERENCE = _('Презентація/конференція')
    SOCIAL_SERVICE_CENTER = _('Центр соціальних служб для сім’ї, дітей та молоді (вкажіть район)')
    CHILD_SERVICE = _('Служба у справах дітей (вкажіть район)')


class EducationTypes(ChoicesEnum):
    SCHOOL = _('Загальноосвітня школа')
    UNIVERSITY = _('Університет, інститут, технікум')
    EXTRA_EDUCATION = _('Додаткові курси, тренінги, семінари')
