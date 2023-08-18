from django.db import models
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel

from simple_history.models import HistoricalRecords
from edc_senaite_interface.model_mixins import SenaiteResultModelMixin, SenaiteResultValueMixin


class CaregiverRequisitionResult(SenaiteResultModelMixin, SiteModelMixin, BaseUuidModel):

    requisition_model = 'flourish_caregiver.caregiverrequisition'

    history = HistoricalRecords()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Sample Result'


class CaregiverResultValue(SenaiteResultValueMixin, BaseUuidModel):

    result = models.ForeignKey(
        CaregiverRequisitionResult, on_delete=models.PROTECT)

    history = HistoricalRecords()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Analysis Result Value'
