from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_visit_tracking.model_mixins import CrfInlineModelMixin

from .antenatal_enrollment import AntenatalEnrollment
from .list_models import ExpenseContributors
from .model_mixins import CrfModelMixin, SocioDemographicDataMixin, HouseHoldDetailsMixin
from ..maternal_choices import CURRENT_OCCUPATION, MONEY_EARNED, MONEY_PROVIDER
from ..maternal_choices import ETHNICITY, HIGHEST_EDUCATION, MARITAL_STATUS


class SocioDemographicData(SocioDemographicDataMixin, CrfModelMixin):
    """ A model completed by the user on Demographics form for all mothers.
    """

    expense_contributors = models.ManyToManyField(
        ExpenseContributors,
        verbose_name='Who in the household contributes to supporting the family '
                     'expenses:',
        blank=True
    )

    @property
    def is_pregnant(self):
        return AntenatalEnrollment.objects.filter(
            subject_identifier=self.subject_identifier).exists()

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = "Socio Demographic Data"
        verbose_name_plural = "Socio Demographic Data"


class HouseHoldDetails(HouseHoldDetailsMixin, BaseUuidModel):
    """ Applicable for twins living in different households.
    """

    parent_model_attr = 'socio_demographics_data'

    socio_demographics_data = models.ForeignKey(
        SocioDemographicData, on_delete=models.CASCADE)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Household Details'
        verbose_name_plural = 'Household Details'
        unique_together = (
            ('socio_demographics_data', 'child_identifier'),)
