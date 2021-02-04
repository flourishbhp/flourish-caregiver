from django.db import models

from edc_base.model_fields import OtherCharField


from .model_mixins import CrfModelMixin

from ..choices import RELATION_TO_INDIVIDUAL, YES_NO_UNK_DWTA


class TbPresenceHouseholdMembers(CrfModelMixin):

    tb_diagnosed = models.CharField(
        verbose_name='Has any member of your household been diagnosed with '
                     'tuberculosis in the last 12 months?',
        max_length=30,
        choices=YES_NO_UNK_DWTA,
        blank=False,
        null=False)

    tb_ind_rel = models.CharField(
        verbose_name='Please indicate the relationship of this individual or '
                     'individuals to you.',
        max_length=20,
        choices=RELATION_TO_INDIVIDUAL,
        blank=True,
        null=True)

    tb_ind_other = OtherCharField(
        verbose_name="if other, specify...",
        max_length=35,
        blank=True,
        null=True)

    cough_signs = models.CharField(
        verbose_name='Has any member of your household had cough for two weeks'
                     ' or more in the last 12 months? ',
        max_length=20,
        choices=YES_NO_UNK_DWTA,
        blank=False,
        null=False)

    cough_ind_rel = models.CharField(
        verbose_name='Please indicate the relationship of this individual or '
                     'individuals to you',
        max_length=20,
        choices=RELATION_TO_INDIVIDUAL,
        blank=True,
        null=True)

    cough_ind_other = OtherCharField(
        verbose_name="if other, specify...",
        max_length=35,
        blank=True,
        null=True)

    fever_signs = models.CharField(
        verbose_name='Has any member of your household had unexplained fever '
                     'concerning for tuberculosis in the last 12 months?',
        max_length=30,
        choices=YES_NO_UNK_DWTA)

    fever_ind_rel = models.CharField(
        verbose_name='Please indicate the relationship of this individual or '
                     'individuals to you',
        max_length=20,
        choices=RELATION_TO_INDIVIDUAL,
        blank=True,
        null=True)

    fever_ind_other = OtherCharField(
        verbose_name="if other, specify...",
        max_length=35,
        blank=True,
        null=True)

    night_sweats = models.CharField(
        verbose_name='Has any member of your household had night sweats in the'
                     ' last 12 months? ',
        max_length=30,
        choices=YES_NO_UNK_DWTA,
        blank=False,
        null=False)

    sweat_ind_rel = models.CharField(
        verbose_name='Please indicate the relationship of this individual or '
                     'individuals to you',
        max_length=20,
        choices=RELATION_TO_INDIVIDUAL,
        blank=True,
        null=True)

    sweat_ind_other = OtherCharField(
        verbose_name="if other, specify...",
        max_length=35,
        blank=True,
        null=True)

    weight_loss = models.CharField(
        verbose_name='Has any member of your household had unexplained weight'
                     ' loss in the last 12 months? ',
        max_length=30,
        choices=YES_NO_UNK_DWTA,
        blank=False,
        null=False)

    weight_ind_rel = models.CharField(
        verbose_name='Please indicate the relationship of this individual or '
                     'individuals to you',
        max_length=20,
        choices=RELATION_TO_INDIVIDUAL,
        blank=True,
        null=True)

    weight_ind_other = OtherCharField(
        verbose_name="if other, specify...",
        max_length=35,
        blank=True,
        null=True)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Presence of TB Symptoms in Household ' \
                       'Members for Pregnant Women'
        verbose_name_plural = 'Presence of TB Symptoms in Household' \
                              ' Members for Pregnant Women'
