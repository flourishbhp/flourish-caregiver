from django.db import models
from ..choices import TB_DRUGS_FREQ, TB_TYPE, YES_NO_UNK_DWTA

from .model_mixins import CrfModelMixin


class TbHistoryPreg(CrfModelMixin):

    prior_tb_infec = models.CharField(
        verbose_name='Do you have a prior history of TB infection?',
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        help_text=('TB infection, known as latent TB, is defined as persons '
                   'who are infected by the bacterium, M. tuberculosis, but '
                   'have no TB symptoms. TB infection is diagnosed with a positive '
                   'tuberculin skin test (TST) or IGRA lab test. '))

    history_of_tbt = models.CharField(
        verbose_name=('Do you have a prior history of taking isoniazid for TB '
                      'preventative therapy (TPT)'),
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    tbt_completed = models.CharField(
        verbose_name='Did you complete your TB preventative therapy (TPT)?',
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        blank=True,
        null=True)

    prior_tb_history = models.CharField(
        verbose_name='Do you have a prior history of TB disease?',
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        help_text=('TB disease, known as active TB, is defined as persons who '
                   'are infected by the bacterium, M. tuberculosis, with TB '
                   'symptoms or positive laboratory findings, such as Gene Xpert '
                   'or sputum culture.'))

    tb_diagnosis_type = models.CharField(
        verbose_name='What type of TB were you diagnosed with?',
        choices=TB_TYPE,
        max_length=30,
        blank=True,
        null=True)

    prior_treatmnt_history = models.CharField(
        verbose_name='Do you have a prior history of taking TB treatment?',
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        help_text='TB treatment generally requires 4 drugs for 6 months or longer.')

    tb_drugs_freq = models.CharField(
        verbose_name='How many drugs did you take for TB treatment?',
        choices=TB_DRUGS_FREQ,
        max_length=30,
        blank=True,
        null=True)

    iv_meds_used = models.CharField(
        verbose_name='Did you take any intravenous (IV) medications during TB treatment?',
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        blank=True,
        null=True)

    tb_treatmnt_completed = models.CharField(
        verbose_name='Did you complete TB treatment? ',
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        blank=True,
        null=True)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'History of TB for Pregnant Women'
        verbose_name_plural = 'History of TB for Pregnant Women'
