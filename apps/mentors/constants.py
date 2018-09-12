from enum import Enum


class ChoicesEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class Religions(ChoicesEnum):
    CHRISTIANITY = 'Christianity'
    CATHOLICISM = 'Catholicism'
    ORTHODOXY = 'Orthodoxy'
    PROTESTANTISM = 'Protestantism'
    JUDAISM = 'Judaism'
    BUDDHISM = 'Buddhism'
    OTHER = 'Other'


class LocalChurchVisitingFrequency(ChoicesEnum):
    ONCE_A_WEEK = 'once_a_week'
    TWICE_A_MONTH = 'twice_a_month'
    ONCE_A_YEAR = 'once_a_year'
    OTHER = 'other'


class MaritalStatuses(ChoicesEnum):
    MARRIED = 'married'
    CIVIL_MARRIAGE = 'civil_marriage'
    DIVORCED = 'divorced'
    WIDOW = 'widow'
    UNMARRIED = 'unmarried'


class Genders(ChoicesEnum):
    MALE = 0
    FEMALE = 1


class HomeTypes(ChoicesEnum):
    APARTMENT = 'apartment'
    PRIVATE_HOUSE = 'private_house'
    RENTED = 'rented'


class AbleToVisitChildFrequency(ChoicesEnum):
    ONCE_A_WEEK = 'once_a_week'
    TWICE_A_MONTH = 'twice_a_month'
    ONCE_A_YEAR = 'once_a_year'
    OTHER = 'other'
