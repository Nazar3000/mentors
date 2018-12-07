import datetime
import time

from django.contrib.postgres.fields import HStoreField, ArrayField
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.constants import MentorStatuses
from .constants import Religions, MaritalStatuses, Genders, HomeTypes, AbleToVisitChildFrequency, \
    MentoringProgramFindOutPlaces, EducationTypes, LocalChurchVisitingFrequency, DocsStatuses, RoadmapDocTypes


class MentorQuestionnaire(models.Model):
    mentor = models.OneToOneField(
        to='users.Mentor',
        on_delete=models.CASCADE,
        related_name='questionnaire'
    )
    creation_date = models.DateTimeField(
        auto_now=True
    )

    # 1. Common data
    full_name = models.CharField(
        max_length=32
    )
    date_of_birth = models.DateField()
    phone_regex = RegexValidator(
        regex=r'\+?1?\d$'
    )
    phone_number = models.CharField(
        max_length=17,
        validators=[phone_regex]
    )
    email = models.EmailField()
    nationality = models.CharField(
        max_length=265
    )
    actual_address = models.CharField(
        max_length=521
    )
    registration_address = models.CharField(
        max_length=521
    )
    religion = models.CharField(
        max_length=20,
        choices=Religions.choices()
    )
    # required if religion value is not Other
    local_church_visiting = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )
    # required if religion value is not Other
    local_church_visiting_frequency = models.CharField(
        max_length=20,
        choices=LocalChurchVisitingFrequency.choices(),
        null=True,
        blank=True
    )

    # 2. Health state
    health_self_estimation = models.CharField(
        max_length=265
    )
    serious_diseases = models.BooleanField(
        default=False
    )
    narcologist = models.BooleanField(
        default=False
    )
    psychiatrist = models.BooleanField(
        default=False
    )
    phthisiatrician = models.BooleanField(
        default=False
    )
    therapist = models.BooleanField(
        default=False
    )
    dermatovenereologist = models.BooleanField(
        default=False
    )
    # required if one of doctors above is True
    hospital_data = models.CharField(
        max_length=512,
        null=True,
        blank=True
    )
    hiv_infected = models.BooleanField(
        default=False
    )

    # 3. Education
    # See MentorQuestionnaireEducation model

    # 4. Job
    # See MentorQuestionnaireJob model

    # 5. Interests, hobbies
    interests_and_hobbies = models.TextField()

    # 6. Marital status
    marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatuses.choices()
    )
    # See MentorQuestionnaireFamilyMember

    # 7. Living conditions
    home_type = models.CharField(
        max_length=20,
        choices=HomeTypes.choices()
    )
    room_count = models.PositiveSmallIntegerField(
        default=1
    )
    people_per_room = models.PositiveSmallIntegerField(
        default=1
    )
    home_family_members_data = models.TextField()
    pets_data = models.TextField()

    # 8. Work with children experience
    # See MentorQuestionnaireChildrenWorkExperience model

    # 9. Want to become a mentor reason
    join_reason = models.TextField()

    # 10. Helpful specifics
    helpful_specifics = models.TextField()

    # 11. Self characteristics
    self_char = models.TextField()

    # 12. Want to help orphan child reason
    want_to_help_reason = models.TextField()

    # 13. Expectations from child
    expectations_from_child = models.TextField()

    # 13.1. Mentoring direction
    socialization = models.BooleanField(
        default=False
    )
    proforientation = models.BooleanField(
        default=False
    )
    help_in_education = models.BooleanField(
        default=False
    )

    # 13.2. Able to visit child frequency
    able_to_visit_frequency = models.CharField(
        max_length=20,
        choices=AbleToVisitChildFrequency.choices()
    )

    # 13.3. Ready for child with disabilities
    ready_for_child_with_disabilities = models.BooleanField(
        default=False
    )

    # 14. Extra data for child safety

    # 14.1. Substances usage
    drink_alcohol = models.BooleanField(
        default=False
    )
    # required if drink_alcohol == True
    drink_alcohol_frequency = models.CharField(
        max_length=64,
        null=True,
        blank=True
    )
    smoke_cigarettes = models.BooleanField(
        default=False
    )
    psychotropic_substances = models.BooleanField(
        default=False
    )
    # required if psychotropic_substances_names == True
    psychotropic_substances_names = models.CharField(
        max_length=256,
        null=True,
        blank=True
    )

    # 14.2. Drug usage
    drug_usage = models.BooleanField(
        default=False
    )
    # required if drug_usage == True
    drug_usage_info = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )

    # 14.3. Have been convicted of crimes related to...?
    crime_convicted = models.BooleanField(
        default=False
    )
    # required if crime_convicted == True
    crime_convicted_description = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )

    # 14.4. Has been previously deprived of parental or guardian rights
    parental_rights_deprived = models.BooleanField(
        default=False
    )
    # required if parental_rights_deprived == True
    parental_rights_deprived_description = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )

    # 15. Allow to use your photos and comments
    allow_to_use_personal_data = models.BooleanField(
        default=True
    )

    # 16. Where the the mentoring program was found out
    program_found_out_place = models.CharField(
        max_length=64,
        choices=MentoringProgramFindOutPlaces.choices()
    )

    # 17.
    convenient_meeting_conditions = models.CharField(
        max_length=128
    )

    def save(self, *args, **kwargs):
        self.mentor.questionnaire_creation_date = self.creation_date
        super().save(*args, **kwargs)


class MentorSocialServiceCenterData(models.Model):
    mentor = models.OneToOneField(
        to='users.Mentor',
        on_delete=models.CASCADE,
        related_name='social_service_center_data'
    )

    infomeeting_date = models.DateField(
        null=True,
        blank=True
    )
    passport_copy = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )
    application = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )
    certificate_of_good_conduct = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )
    medical_certificate = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )
    psychologist_meeting_date = models.DateField(
        null=True,
        blank=True
    )
    psychologist_summary = models.TextField(
        null=True,
        blank=True
    )
    recommended_to_training = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )
    training_date = models.DateField(
        null=True,
        blank=True
    )
    trainer_summary = models.TextField(
        null=True,
        blank=True
    )
    admitted_to_child = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )
    contract_number = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    contract_date = models.DateField(
        null=True,
        blank=True
    )
    comment = models.TextField(
        null=True,
        blank=True
    )

    @property
    def docs_status(self):
        docs_fields_values = [
            self.passport_copy,
            self.application,
            self.certificate_of_good_conduct,
            self.medical_certificate
        ]
        if all(value for value in docs_fields_values):
            return DocsStatuses.ALL.name
        elif any(value for value in docs_fields_values):
            return DocsStatuses.NOT_ALL.name
        else:
            return DocsStatuses.NOTHING.name

    def save(self, *args, **kwargs):
        # set mentor status
        if self.infomeeting_date and self.mentor.status == MentorStatuses.NOT_SPECIFIED:
            self.mentor.status = MentorStatuses.PASSED_INFO_MEETING
        if self.training_date \
                and self.mentor.status in (MentorStatuses.NOT_SPECIFIED, MentorStatuses.PASSED_INFO_MEETING):
            self.mentor.status = MentorStatuses.PASSED_TRAINING
        if self.psychologist_meeting_date \
                and self.mentor.status in (
                    MentorStatuses.NOT_SPECIFIED,
                    MentorStatuses.PASSED_INFO_MEETING,
                    MentorStatuses.PASSED_TRAINING):
            self.mentor.status = MentorStatuses.PASSED_INTERVIEW_WITH_PSYCHOLOGIST
        if self.mentor.mentoree \
            and self.mentor.status in (
                MentorStatuses.NOT_SPECIFIED,
                MentorStatuses.PASSED_INFO_MEETING,
                MentorStatuses.PASSED_TRAINING,
                MentorStatuses.PASSED_INTERVIEW_WITH_PSYCHOLOGIST):
            self.mentor.status = MentorStatuses.SELECTED_FOR_MENTOREE
        if self.mentor.meetings.count() \
            and self.mentor.status in (
                MentorStatuses.NOT_SPECIFIED,
                MentorStatuses.PASSED_INFO_MEETING,
                MentorStatuses.PASSED_TRAINING,
                MentorStatuses.PASSED_INTERVIEW_WITH_PSYCHOLOGIST,
                MentorStatuses.SELECTED_FOR_MENTOREE):
            self.mentor.status = MentorStatuses.ACTIVE_INTERACTION

        super().save(*args, **kwargs)


class MentorQuestionnaireEducation(models.Model):
    questionnaire = models.ForeignKey(
        to=MentorQuestionnaire,
        on_delete=models.CASCADE
    )
    education_type = models.CharField(
        max_length=20,
        choices=EducationTypes.choices()
    )
    institution = models.CharField(
        max_length=256,
        blank=True,
        default=''
    )
    year_of_admission = models.PositiveIntegerField()
    year_of_graduation = models.PositiveIntegerField()
    degree = models.CharField(
        max_length=256
    )


MONTHYEAR_INPUT_FORMATS = (
    '%m-%Y', '%m/%Y', '%m/%y', '%m.%Y'  # '10-2006', '2006/10', '10/06', 10.2006
)


class MonthYearField(models.CharField):
    default_error_messages = {
        'invalid': _('Введіть валідний місяць і рік.'),
    }
    max_length = 7

    def __init__(self, input_formats=None, *args, **kwargs):
        kwargs['max_length'] = self.max_length
        super().__init__(*args, **kwargs)
        self.input_formats = input_formats

    def clean(self, value, *args):
        if value in validators.EMPTY_VALUES:
            return None
        if isinstance(value, datetime.datetime):
            return format(value, '%m-%Y')
        if isinstance(value, datetime.date):
            return format(value, '%m-%Y')
        for fmt in self.input_formats or MONTHYEAR_INPUT_FORMATS:
            try:
                date = datetime.date(*time.strptime(value, fmt)[:3])
                return format(date, '%m-%Y')
            except ValueError:
                continue
        raise ValidationError(self.error_messages['invalid'])


class MentorQuestionnaireJob(models.Model):
    questionnaire = models.ForeignKey(
        to=MentorQuestionnaire,
        on_delete=models.CASCADE
    )
    is_current = models.BooleanField(
        default=False
    )

    organization_name = models.CharField(
        max_length=512
    )
    date_since = MonthYearField()
    date_till = MonthYearField()
    contact_info = models.CharField(
        max_length=512
    )
    position = models.CharField(
        max_length=512
    )
    duties = models.CharField(
        max_length=512
    )
    reason_for_leaving = models.CharField(
        max_length=512
    )


class MentorQuestionnaireFamilyMember(models.Model):
    questionnaire = models.ForeignKey(
        to=MentorQuestionnaire,
        on_delete=models.CASCADE
    )

    name = models.CharField(
        max_length=512
    )
    gender = models.CharField(
        max_length=10,
        choices=Genders.choices()
    )
    date_of_birth = models.DateField()
    relation = models.CharField(
        max_length=64
    )


class MentorQuestionnaireChildrenWorkExperience(models.Model):
    questionnaire = models.ForeignKey(
        to=MentorQuestionnaire,
        on_delete=models.CASCADE
    )

    organization_name = models.CharField(
        max_length=256
    )
    date_since = MonthYearField()
    date_till = MonthYearField()
    contact_info = models.CharField(
        max_length=512
    )
    position = models.CharField(
        max_length=512
    )
    duties = models.CharField(
        max_length=512
    )
    children_age_group = models.CharField(
        max_length=64
    )


class MentorLicenceKey(models.Model):
    key_validator = RegexValidator(
        regex=r'\d{3}[a-zA-z]{3}')
    key = models.CharField(
        max_length=10,
        validators=[key_validator])


class Mentoree(models.Model):
    first_name = models.CharField(
        max_length=32)
    last_name = models.CharField(
        max_length=32,
        null=True,
        blank=True)
    date_of_birth = models.DateField(
        null=True,
        blank=True)
    dream = models.CharField(
        max_length=128,
        null=True,
        blank=True)
    want_to_become = models.CharField(
        max_length=32,
        null=True,
        blank=True)
    fears = models.CharField(
        max_length=128,
        null=True,
        blank=True)
    loves = models.CharField(
        max_length=64,
        null=True,
        blank=True)
    hates = models.CharField(
        max_length=64,
        null=True,
        blank=True)
    strengths = models.CharField(
        max_length=64,
        null=True,
        blank=True)
    extra_data = models.CharField(
        max_length=128,
        null=True,
        blank=True)
    organization = models.ForeignKey(
        to='users.Organization',
        on_delete=models.SET_NULL,
        null=True)
    profile_image = models.ImageField(
        upload_to='mentorees/profile',
        null=True,
        blank=True)
    extra_data_fields = ArrayField(
        HStoreField(
            default=dict),
        null=True,
        blank=True)

    story = models.TextField(
        null=True,
        blank=True)

    def save(self, *args, **kwargs):
        if not self.extra_data_fields:
            self.extra_data_fields = [
                {_('Гігієна'): ''},
                {_('Що цій дитині допоможе бути самостійним'): ''},
                {_('Емоціанальний стан дитини'): ''},
                {_('Навички спілкування'): ''},
                {_('Як орієнтується в просторі (чи є проблеми)'): ''}
            ]

        super().save(*args, **kwargs)


class StoryImage(models.Model):
    # TODO: find out how many images should be available to upload
    mentoree = models.ForeignKey(
        to=Mentoree,
        on_delete=models.CASCADE,
        related_name='story_images')
    image = models.ImageField(
        upload_to='mentorees/story')


class Meeting(models.Model):
    performer = models.ForeignKey(
        to='users.Mentor',
        on_delete=models.CASCADE,
        related_name='meetings')
    title = models.CharField(
        max_length=16)
    date = models.DateField()
    description = models.TextField()
    observation = models.TextField()
    note_for_next_meeting = models.TextField()


class MeetingImage(models.Model):
    # TODO: find out how many images should be available to upload
    meeting = models.ForeignKey(
        to=Meeting,
        on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='mentorees/meeting')


class Post(models.Model):
    author = models.ForeignKey(
        to='users.Mentor',
        on_delete=models.CASCADE,
        related_name='posts')
    content = models.TextField()
    image = models.ImageField(
        upload_to='mentorees/post',
        null=True,
        blank=True)
    likes = models.ManyToManyField(
        to='users.Mentor')
    datetime = models.DateTimeField(
        auto_now=True)


class PostComment(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments')
    datetime = models.DateTimeField(
        auto_now=True)
    author = models.ForeignKey(
        to='users.Mentor',
        on_delete=models.CASCADE)
    content = models.TextField()


class Proforientation(models.Model):
    related_mentor = models.ManyToManyField(
        to='users.Mentor'
    )

    company_name = models.CharField(
        max_length=256
    )
    profession_name = models.CharField(
        max_length=256
    )
    address = models.CharField(
        max_length=512
    )
    meeting_days = models.CharField(
        max_length=128
    )
    business_description = models.TextField()
    phone_regex = RegexValidator(
        regex=r'\+?1?\d$')
    phone_number = models.CharField(
        max_length=17,
        validators=[phone_regex])


class MIA(models.Model):
    tsc_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=2048)
    schedule = models.CharField(max_length=2048)
    phone_number_fax_str = models.CharField(max_length=2048)
    email = models.EmailField()
    region = models.CharField(max_length=2048)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)


class RoadmapDoc(models.Model):
    doc_type = models.CharField(
        max_length=15,
        choices=RoadmapDocTypes.choices()
    )
    file = models.FileField(
        upload_to='mentorees/roadmap_docs'
    )


class Question(models.Model):
    mentor = models.ForeignKey(
        to='users.Mentor',
        on_delete=models.CASCADE
    )
    body = models.TextField()
