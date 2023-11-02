from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager

from .eligibility import PregWomenEligibility
from .model_mixins import SearchSlugModelMixin
from ..identifiers import ScreeningIdentifier


class ScreeningPregWomenManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, eligibility_identifier):
        return self.get(screening_identifier=eligibility_identifier)


class ScreeningPregWomen(NonUniqueSubjectIdentifierFieldMixin, SiteModelMixin,
                         SearchSlugModelMixin, BaseUuidModel):
    identifier_cls = ScreeningIdentifier

    screening_identifier = models.CharField(
        verbose_name='Eligibility Identifier',
        max_length=36,
        blank=True,
        null=True,
        unique=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=get_utcnow,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        null=True,
        editable=False,
        help_text='Date and time of assessing eligibility')

    hiv_testing = models.CharField(
        verbose_name=('If HIV status not known, are you willing to undergo HIV'
                      ' testing and counseling?'),
        choices=YES_NO,
        null=True,
        editable=False,
        max_length=3)

    breastfeed_intent = models.CharField(
        verbose_name='Do you intend on breastfeeding your infant?',
        choices=YES_NO,
        null=True,
        editable=False,
        max_length=3)

    ineligibility = models.TextField(
        verbose_name='Reason not eligible',
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    # is updated via signal once subject is consented
    is_consented = models.BooleanField(
        default=False,
        editable=False)

    history = HistoricalRecords()

    objects = ScreeningPregWomenManager()

    def __str__(self):
        return f'{self.screening_identifier}'

    def save(self, *args, **kwargs):
        if not self.screening_identifier:
            self.screening_identifier = self.identifier_cls().identifier

        super().save(*args, **kwargs)

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('screening_identifier')
        return fields

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Screening for Newly Enrolled Pregnant Women'
        verbose_name_plural = 'Screening for Newly Enrolled Pregnant Women'


class ScreeningPregWomenInline(BaseUuidModel):
    mother_screening = models.ForeignKey(
        ScreeningPregWomen,
        on_delete=models.PROTECT)

    child_subject_identifier = models.CharField(
        verbose_name='Child Subject Identifier',
        max_length=36,
        blank=True,
        null=True,
        unique=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=get_utcnow,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        help_text='Date and time of assessing eligibility')

    hiv_testing = models.CharField(
        verbose_name=('If HIV status not known, are you willing to undergo HIV'
                      ' testing and counseling?'),
        choices=YES_NO,
        max_length=3)

    breastfeed_intent = models.CharField(
        verbose_name='Do you intend on breastfeeding your infant?',
        choices=YES_NO,
        max_length=3)

    ineligibility = models.TextField(
        verbose_name='Reason not eligible',
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    is_consented = models.BooleanField(
        default=False,
        editable=False)

    def save(self, *args, **kwargs):
        eligibility_criteria = PregWomenEligibility(
            self.hiv_testing, self.breastfeed_intent)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        super().save(*args, **kwargs)

    def __str__(self):
        return (f'{self.mother_screening.screening_identifier}'
                f' {self.child_subject_identifier}')

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Screening Pregnant Women Inline'
        verbose_name_plural = 'Screening Pregnant Women Inlines'
