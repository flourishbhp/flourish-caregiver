from django.db import models
from edc_constants.choices import YES_NO

from flourish_caregiver.models.model_mixins import CrfModelMixin


class ScreenToTbStudy(CrfModelMixin):
    tb_participation = models.CharField(
        verbose_name='Participant willing to do an Informed consent for the Tb Study',
        help_text='Illegible for TB study is NO',
        choices=YES_NO,
        max_length=10,
        default=''
    )


    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Study Screening Form'
        verbose_name_plural = 'TB Study Screening Forms'
