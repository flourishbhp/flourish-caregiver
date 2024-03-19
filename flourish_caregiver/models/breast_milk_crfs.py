from django.db import models

from .list_models import MestitisCN1Actions, MestitisCN2Actions, MestitisCN3Actions, \
    MestitisCN4Actions, MestitisCN5Actions, MestitisM1Actions, \
    MestitisM2Actions, \
    MestitisM3Actions, \
    MestitisM4Actions, \
    MestitisM5Actions
from .model_mixins.breast_milk_field_mixin import \
    BreastMilkFieldsMixin


class BreastMilkBirth(BreastMilkFieldsMixin, models.Model):
    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = "Breast Milk Collection CRF at Birth Visit"
        verbose_name_plural = "Breast Milk Collection CRF at Birth Visit"


class BreastMilk6Months(BreastMilkFieldsMixin, models.Model):
    mastitis_1_action = models.ManyToManyField(
        MestitisM1Actions,
        verbose_name='What did the mother do (first instance)? ',
        max_length=20,
        related_name='mastitis_1_actions_6months',
        blank=True
    )

    mastitis_2_action = models.ManyToManyField(
        MestitisM2Actions,
        verbose_name='What did the mother do (second instance)? ',
        max_length=20,
        related_name='mastitis_2_actions_6months',
        blank=True
    )

    mastitis_3_action = models.ManyToManyField(
        MestitisM3Actions,
        verbose_name='What did the mother do (third instance)? ',
        max_length=20,
        related_name='mastitis_3_actions_6months',
        blank=True
    )

    mastitis_4_action = models.ManyToManyField(
        MestitisM4Actions,
        verbose_name='What did the mother do (fourth instance)? ',
        max_length=20,
        related_name='mastitis_4_actions_6months',
        blank=True
    )

    mastitis_5_action = models.ManyToManyField(
        MestitisM5Actions,
        related_name='mastitis_5_actions_6months',
        verbose_name='What did the mother do (fifth instance)? ',
        max_length=20,
        blank=True
    )

    cracked_nipples_1_action = models.ManyToManyField(
        MestitisCN1Actions,
        verbose_name='What did the mother do when experiencing cracked nipples (first '
                     'instance)? ',
        max_length=20,
        related_name='cracked_nipples_1_actions_6months',
        blank=True
    )

    cracked_nipples_2_action = models.ManyToManyField(
        MestitisCN2Actions,
        verbose_name='What did the mother do when experiencing cracked nipples (second '
                     'instance)? ',
        max_length=20,
        related_name='cracked_nipples_2_actions_6months',
        blank=True
    )

    cracked_nipples_3_action = models.ManyToManyField(
        MestitisCN3Actions,
        verbose_name='What did the mother do when experiencing cracked nipples (third '
                     'instance)? ',
        max_length=20,
        related_name='cracked_nipples_3_actions_6months',
        blank=True
    )

    cracked_nipples_4_action = models.ManyToManyField(
        MestitisCN4Actions,
        verbose_name='What did the mother do when experiencing cracked nipples (fourth '
                     'instance)? ',
        max_length=20,
        related_name='cracked_nipples_4_actions_6months',
        blank=True
    )

    cracked_nipples_5_action = models.ManyToManyField(
        MestitisCN5Actions,
        verbose_name='What did the mother do when experiencing cracked nipples (fifth '
                     'instance)? ',
        max_length=20,
        related_name='cracked_nipples_5_actions_6months',
        blank=True
    )

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = "Breast Milk Collection CRF at 6-Month "
        verbose_name_plural = "Breast Milk Collection CRF at 6-Month "
