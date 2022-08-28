from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from flourish_caregiver.choices import REASONS_NOT_PARTICIPATING
from flourish_caregiver.models.model_mixins import CrfModelMixin


class TbStudyEligibility(CrfModelMixin):
    tb_participation = models.CharField(
        verbose_name='Participant willing to do an Informed consent for the Tb Study',
        help_text='Illegible for TB study is NO',
        choices=YES_NO,
        max_length=10,
        default=''
    )

    # reasons_not_participating = models.CharField(
    #     verbose_name='Reasons unable to obtain an informed consent for TB study',
    #     help_text='if <22 weeks GA or Still thinking, The form should appear at 2000D/ '
    #               '2001',
    #     choices=REASONS_NOT_PARTICIPATING,
    #     max_length=50,
    #     blank=True,
    #     null=True
    # )
    #
    # reasons_not_participating_other = OtherCharField()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Study Screening Form'
        verbose_name_plural = 'TB Study Screening Forms'
