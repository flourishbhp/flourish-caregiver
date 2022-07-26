from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import date_not_future
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import NOT_APPLICABLE

from .model_mixins import CrfModelMixin
from .model_mixins.martenal_arv_table_mixin import MaternalArvTableMixin
from ..choices import ARV_INTERRUPTION_REASON


class MaternalArvAtDelivery(CrfModelMixin):
    """ This model is for all HIV positive mothers who
       have just delivered
       """

    last_visit_change = models.CharField(
        verbose_name='Was there any change or interruption in the ARVs received during '
                     'pregnancy since the enrolment visit through delivery?',
        max_length=20,
        choices=YES_NO
    )

    change_reason = models.CharField(
        verbose_name='Please give reason for the change or interruption',
        max_length=35,
        choices=ARV_INTERRUPTION_REASON,
        default=NOT_APPLICABLE
    )

    change_reason_other = OtherCharField()

    resume_treat = models.CharField(
        verbose_name='If interruption occurred after enrolment visit, did the participant'
                     ' resume the ARV treatment?',
        max_length=35,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE
    )


    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Maternal ARV At Delivery'
        verbose_name_plural = 'Maternal ARV At Delivery'


class MaternalArvTableAtDelivery(MaternalArvTableMixin):
    """ Inline ARV table to indicate ARV medication taken by mother """

    maternal_arv_at_delivery = models.ForeignKey(MaternalArvAtDelivery, on_delete=PROTECT)

    date_resumed = models.DateField(
        verbose_name="Date Stopped",
        validators=[date_not_future],
        null=True,
        blank=True)


    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Maternal ARV Table At Delivery'
        verbose_name_plural = 'Maternal ARV Table At Delivery'
