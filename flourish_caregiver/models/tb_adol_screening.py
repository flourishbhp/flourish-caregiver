from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from flourish_caregiver.choices import REASONS_UNWILLING_ADOL
from flourish_caregiver.models.model_mixins import CrfModelMixin


class TbAdolEligibility(CrfModelMixin):

    tb_adol_participation = models.CharField(
        verbose_name=('Participant willing to do an Informed consent for the '
                      'TB Adolescent Study'),
        help_text='Illegible for TB adolescent study if NO',
        choices=YES_NO,
        max_length=10,)

    reasons_unwilling_part = models.CharField(
        verbose_name='Reasons unable to obtain an informed consent for TB study',
        choices=REASONS_UNWILLING_ADOL,
        max_length=50,
        blank=True,
        null=True
    )

    reasons_unwilling_part_other = OtherCharField()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Adolescent Study Screening'
