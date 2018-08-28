class UserTypes:
    GOVERN_USER = 0
    MENTOR = 1
    SOCIAL_SERVICE_CENTER = 2
    PUBLIC_SERVICE = 3
    INSTITUTION = 4
    CHILD_SERVICE = 5
    PROJECT_ASSISTANT = 6

    USER_TYPE_CHOICES = (
        (GOVERN_USER, 'govern_user'),
        (MENTOR, 'mentor'),
        (SOCIAL_SERVICE_CENTER, 'social_service_center'),
        (PUBLIC_SERVICE, 'public_service'),
        (INSTITUTION, 'institution'),
        (CHILD_SERVICE, 'child_service'),
        (PROJECT_ASSISTANT, 'project_assistant'),
    )
