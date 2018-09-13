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


class MentoringProgramFindOutPlaces(ChoicesEnum):
    TV = 'tv'
    RADIO = 'radio'
    OTHER_MEDIA = 'other_media'
    FACEBOOK_OR_OTHER_SOCIAL_NETWORKS = 'facebook_or_other_social_networks'
    INTERNET = 'internet'
    FRIENDS_RELATIVES_ACQUAINTANCES = 'friends_relatives_acquaintances'
    PAPERS = 'papers'
    PRESENTATION_CONFERENCE = 'presentation_conference'
    SOCIAL_SERVICE_CENTER = 'social_service_center'
    CHILD_SERVICE = 'child_service'
