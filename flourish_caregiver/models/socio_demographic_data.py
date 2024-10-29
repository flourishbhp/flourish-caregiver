from django.db import models
from edc_base.model_mixins import BaseUuidModel

from .antenatal_enrollment import AntenatalEnrollment
from .list_models import ExpenseContributors
from .model_mixins import CrfModelMixin, SocioDemographicDataMixin, HouseHoldDetailsMixin

from ..helper_classes.utils import get_child_subject_identifier_by_visit


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
    def child_subject_identifier(self):
        return get_child_subject_identifier_by_visit(self.maternal_visit)

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
