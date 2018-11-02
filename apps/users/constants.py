from enum import Enum

from django.utils.translation import gettext_lazy as _


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
    SOCIAL_POLICY_MINISTRY = 7

    USER_TYPE_CHOICES = (
        (GOVERN_USER, 'govern_user'),
        (MENTOR, 'mentor'),
        (SOCIAL_SERVICE_CENTER, 'social_service_center'),
        (PUBLIC_SERVICE, 'public_service'),
        (ORGANIZATION, 'organization'),
        (CHILD_SERVICE, 'child_service'),
        (VOLUNTEER, 'volunteer'),
        (SOCIAL_POLICY_MINISTRY, 'social_policy_ministry'),
    )


class MentorStatuses(ChoicesEnum):
    NOT_SPECIFIED = _('Не визначений')
    PASSED_INFO_MEETING = _('Пройшов інфо-зустріч')
    PASSED_TRAINING = _('Пройшов тренінг')
    REJECTED_TO_BE_MENTOR = _('Відмовився бути наставником')
    PASSED_INTERVIEW_WITH_PSYCHOLOGIST = _('Пройшов співбесіду з психологом')
    SELECTED_FOR_MENTOREE = _('Підібраний для вихованця')
    ACTIVE_INTERACTION = _('Активна взаємодія')
    PAIR_DISBANDED = _('Пара розформована')
