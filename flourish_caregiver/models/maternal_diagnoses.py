from django.db import models
from edc_base.model_fields import OtherCharField

from edc_constants.choices import YES_NO_NA, YES_NO

from .model_mixins import CrfModelMixin
from .list_models import WcsDxAdult, MaternalDiagnosesList


class MaternalDiagnoses(CrfModelMixin):

    new_diagnoses = models.CharField(
        max_length=25,
        verbose_name='Have there been any new diagnoses or '
                     'medical problems in the mother\'s health since last visit?',
        choices=YES_NO,
    )

    diagnoses = models.ManyToManyField(
        MaternalDiagnosesList,
        verbose_name="Have any of the following diagnoses"
                     " occured since last visit?",
        blank=True,
    )

    diagnoses_other = OtherCharField(
        max_length=35,
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    has_who_dx = models.CharField(
        verbose_name=(
            "During this pregnancy, did the mother have any new diagnoses "
            "listed in the WHO Adult/Adolescent HIV clinical staging document "
            "which  is/are NOT reported?"),
        max_length=3,
        choices=YES_NO_NA)

    who = models.ManyToManyField(
        WcsDxAdult,
        verbose_name='List any new WHO Stage III/IV diagnoses '
        'that are not reported in the Question above:'
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = "Maternal Diagnosis"
        verbose_name_plural = "Maternal Diagnoses"
