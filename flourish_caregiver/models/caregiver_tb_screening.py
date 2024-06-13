from django.db import models
from edc_base.model_mixins import BaseUuidModel

from flourish_caregiver.choices import YES_NO_AR_OTHER
from flourish_caregiver.helper_classes import MaternalStatusHelper
from flourish_caregiver.helper_classes.tb_diagnosis import TBDiagnosis
from flourish_caregiver.models.model_mixins import CrfModelMixin
from flourish_caregiver.models.model_mixins.flourish_tb_screening_mixin import \
    TBScreeningMixin
from flourish_child.choices import YES_NO_OTHER


class CaregiverTBScreening(CrfModelMixin, TBScreeningMixin):
    diagnosed_with_TB = models.CharField(
        verbose_name='Were you diagnosed with TB?',
        choices=YES_NO_AR_OTHER,
        max_length=25,
        blank=True,
        null=True
    )
    diagnosed_with_TB_other = models.TextField(
        verbose_name='If Other, please specify',
        blank=True, null=True)

    started_on_TB_treatment = models.CharField(
        verbose_name='Were you started on TB treatment?',
        choices=YES_NO_OTHER,
        max_length=15,
        blank=True,
        null=True)

    started_on_TB_treatment_other = models.TextField(
        verbose_name='If Other, please specify',
        blank=True, null=True)

    started_on_TB_preventative_therapy = models.CharField(
        verbose_name='Were you started on TB preventative therapy?',
        choices=YES_NO_OTHER,
        max_length=15,
        blank=True,
        null=True)

    started_on_TB_preventative_therapy_other = models.TextField(
        verbose_name='If Other, please specify',
        blank=True, null=True)

    def save(self, *args, **kwargs):
        maternal_status_helper = MaternalStatusHelper(maternal_visit=self.maternal_visit)
        tb_diagnoses = TBDiagnosis(hiv_status=maternal_status_helper.hiv_status)

        self.tb_diagnoses = tb_diagnoses.evaluate_for_tb(self)

        super().save(*args, **kwargs)

    class Meta(BaseUuidModel.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver TB Screening'
        verbose_name_plural = 'Caregiver TB Screenings'
