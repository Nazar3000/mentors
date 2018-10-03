from enum import Enum


class ChoicesEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class UserTypes:
    GOVERN_USER = 0
    MENTOR = 1
    SOCIAL_SERVICE_CENTER = 2
    PUBLIC_SERVICE = 3
    ORGANIZATION = 4
    CHILD_SERVICE = 5
    VOLUNTEER = 6

    USER_TYPE_CHOICES = (
        (GOVERN_USER, 'govern_user'),
        (MENTOR, 'mentor'),
        (SOCIAL_SERVICE_CENTER, 'social_service_center'),
        (PUBLIC_SERVICE, 'public_service'),
        (ORGANIZATION, 'organization'),
        (CHILD_SERVICE, 'child_service'),
        (VOLUNTEER, 'volunteer'),
    )
