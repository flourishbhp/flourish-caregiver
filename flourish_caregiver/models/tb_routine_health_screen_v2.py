from django.db import models
from edc_base.model_mixins import BaseUuidModel

from ..choices import YES_NO_UNK_DWTA, VISIT_NUMBER
from .list_models import TbVisitCareLocation
from .model_mixins import CrfModelMixin


class TbRoutineHealthScreenV2(CrfModelMixin):
    tb_health_visits = models.CharField(
        verbose_name=('How many health visits did you have in the last year '
                      'since last study visit?'),
        max_length=20,
        choices=VISIT_NUMBER,
        help_text=('if 0, end of CRF. If 1 or greater,'
                   ' embed follow up questions for each visit.')
    )

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Screen for TB at routine health encounters V2'
        verbose_name_plural = 'Screen for TB at routine health encounters V2'


class TbRoutineHealthEncounters(BaseUuidModel):
    routine_encounter = models.ForeignKey(TbRoutineHealthScreenV2, on_delete=models.PROTECT,
                                          related_name='routine_encounter', )
    screen_location = models.ManyToManyField(
        TbVisitCareLocation,
        blank=True,
        verbose_name="For visit #1, where did you receive care",
    )

    screen_location_other = models.TextField(
        verbose_name='If other, specify',
        max_length=150,
        blank=True,
        null=True)

    tb_screened = models.CharField(
        verbose_name='For this healthcare visit, were you screened for'
                     ' TB with the four screening questions'
                     ' (cough,fever, weight loss, night sweats)?',
        max_length=20,
        choices=YES_NO_UNK_DWTA,
        help_text="If yes, continue to Q5 If no/I don’t know/prefer not to answer,"
                  "CRF complete if no further visits, "
                  "else repeat questions 2-6 for each healthcare visit reported in question 1 "
    )
    pos_screen = models.CharField(
        verbose_name="Did you screen positive for TB at this visit"
                     " because you had cough, fever, weight loss, "
                     "and/or night sweats? ",
        max_length=20,
        choices=YES_NO_UNK_DWTA,
        help_text="If no/I don’t know/prefer not to answer, CRF complete if no further visits"
    )

    diagnostic_referral = models.CharField(
        verbose_name='Were you referred to another clinic for further evaluation'
                     ' or did you receive testing during '
                     'that visit to see if you had tuberculosis?',
        max_length=20,
        null=True,
        blank=True,
        choices=YES_NO_UNK_DWTA)

    class Meta:
        verbose_name = 'TB Routine Health Encounters Inline'
        app_label = 'flourish_caregiver'

