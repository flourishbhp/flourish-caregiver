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
        null=True)

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

    tb_referral = models.CharField(
        verbose_name='Were you referred to a TB clinic in the last 12 months? ',
        max_length=30,
        choices=YES_NO_UNK_DWTA,
        null=True)

    tb_in_house = models.CharField(
        verbose_name='Has any member of your household that was not diagnosed with TB '
                     'had cough for two weeks or more in the last 12 months? ',
        max_length=20,
        choices=YES_NO_UNK_DWTA,
        null=True)

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
        verbose_name='Has any member of your household that was not diagnosed with TB had'
                     ' unexplained fever concerning for tuberculosis in the last 12 '
                     'months? ',
        max_length=30,
        choices=YES_NO_UNK_DWTA,
        null=True)

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
        verbose_name='Has any member of your household that was not diagnosed with TB '
                     'had night sweats in the last 12 months? ',
        help_text=('A person is considered to have night sweats if they have had more '
                   'than two nights of waking up with their night clothing drenched due '
                   'to sweating with a need to change the night clothing. '),
        max_length=30,
        choices=YES_NO_UNK_DWTA,
        null=True)

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
        verbose_name='Has any member of your household that was not diagnosed with TB  '
                     'had unexplained weight loss in the last 12 months?',
        max_length=30,
        choices=YES_NO_UNK_DWTA,
        null=True)

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
        verbose_name = 'TB symptoms in household members at 2 months postpartum'
        verbose_name_plural = 'TB symptoms in household members at 2 months postpartum'
