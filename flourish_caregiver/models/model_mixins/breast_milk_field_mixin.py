from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from flourish_caregiver.choices import BREAST_COLLECTED_CHOICES, EXP_COUNT_CHOICES, \
    MASTITIS_TYPE_CHOICES, \
    NOT_COLLECTED_REASONS_CHOICES, YES_RESOLVED_NO
from . import CrfModelMixin
from ..list_models import MestitisActions


class BreastMilkFieldsMixin(CrfModelMixin, models.Model):
    exp_mastitis = models.CharField(
        verbose_name="Since the last FLOURISH visit (birth visit), has the participant "
                     "experienced mastitis?",
        choices=YES_RESOLVED_NO,
        max_length=35,
        null=True
    )

    exp_mastitis_count = models.CharField(
        verbose_name="How many times has the participant experienced mastitis since the "
                     "last visit?",
        max_length=10,
        choices=EXP_COUNT_CHOICES,
        null=True,
        blank=True
    )

    mastitis_1_date_onset = models.DateField(
        verbose_name='Approximate date of onset of mastitis (first instance): ',
        null=True,
        blank=True
    )

    mastitis_1_type = models.CharField(
        verbose_name='Is the mastitis(first instance):',
        max_length=20,
        choices=MASTITIS_TYPE_CHOICES,
        null=True,
        blank=True
    )

    mastitis_1_action = models.ManyToManyField(
        MestitisActions,
        verbose_name='What did the mother do (first instance)? ',
        max_length=20,
        related_name='mastitis_1_actions',
        blank=True
    )

    mastitis_1_action_other = OtherCharField(
        verbose_name='If Other, specify (first instance)'
    )

    mastitis_2_date_onset = models.DateField(
        verbose_name='Approximate date of onset of mastitis (second instance):',
        null=True,
        blank=True
    )

    mastitis_2_type = models.CharField(
        verbose_name='Is the mastitis(second instance):',
        max_length=20,
        choices=MASTITIS_TYPE_CHOICES,
        null=True,
        blank=True
    )

    mastitis_2_action = models.ManyToManyField(
        MestitisActions,
        verbose_name='What did the mother do (second instance)? ',
        max_length=20,
        related_name='mastitis_2_actions',
        blank=True
    )

    mastitis_2_action_other = OtherCharField(
        verbose_name='If Other, specify (second instance)'
    )

    mastitis_3_date_onset = models.DateField(
        verbose_name='Approximate date of onset of mastitis (third instance):',
        null=True,
        blank=True
    )

    mastitis_3_type = models.CharField(
        verbose_name='Is the mastitis(third instance):',
        max_length=20,
        choices=MASTITIS_TYPE_CHOICES,
        null=True,
        blank=True
    )

    mastitis_3_action = models.ManyToManyField(
        MestitisActions,
        verbose_name='What did the mother do (third instance)? ',
        max_length=20,
        related_name='mastitis_3_actions',
        blank=True
    )

    mastitis_3_action_other = OtherCharField(
        verbose_name='If Other, specify (third instance)'
    )

    mastitis_4_date_onset = models.DateField(
        verbose_name='Approximate date of onset of mastitis (fourth instance):',
        null=True,
        blank=True
    )

    mastitis_4_type = models.CharField(
        verbose_name='Is the mastitis(fourth instance):',
        max_length=20,
        choices=MASTITIS_TYPE_CHOICES,
        null=True,
        blank=True
    )

    mastitis_4_action = models.ManyToManyField(
        MestitisActions,
        verbose_name='What did the mother do (fourth instance)? ',
        max_length=20,
        related_name='mastitis_4_actions',
        blank=True
    )

    mastitis_4_action_other = OtherCharField(
        verbose_name='If Other, specify (fourth instance)'
    )

    mastitis_5_date_onset = models.DateField(
        verbose_name='Approximate date of onset of mastitis (fifth instance):',
        null=True,
        blank=True
    )

    mastitis_5_type = models.CharField(
        verbose_name='Is the mastitis(fifth instance):',
        max_length=20,
        choices=MASTITIS_TYPE_CHOICES,
        null=True,
        blank=True
    )

    mastitis_5_action = models.ManyToManyField(
        MestitisActions,
        related_name='mastitis_5_actions',
        verbose_name='What did the mother do (fifth instance)? ',
        max_length=20,
        blank=True
    )

    mastitis_5_action_other = OtherCharField(
        verbose_name='If Other, specify (fifth instance)'
    )

    exp_cracked_nipples = models.CharField(
        verbose_name='Has the participant experienced cracked nipples since the last '
                     'FLOURISH visit?',
        choices=YES_NO,
        max_length=10,
        null=True,
    )

    exp_cracked_nipples_count = models.CharField(
        verbose_name="How many times has the participant experienced cracked nipples?",
        max_length=10,
        choices=EXP_COUNT_CHOICES,
        null=True,
        blank=True
    )

    cracked_nipples_1_date_onset = models.DateField(
        verbose_name='Approximate date of onset of cracked nipples (first instance): ',
        null=True,
        blank=True
    )

    cracked_nipples_1_type = models.CharField(
        verbose_name='Are the cracked nipples (first instance):',
        max_length=20,
        choices=MASTITIS_TYPE_CHOICES,
        null=True,
        blank=True
    )

    cracked_nipples_1_action = models.ManyToManyField(
        MestitisActions,
        verbose_name='What did the mother do when experiencing cracked nipples (first '
                     'instance)? ',
        max_length=20,
        related_name='cracked_nipples_1_actions',
        blank=True
    )

    cracked_nipples_1_action_other = OtherCharField(
        verbose_name='If Other, specify (first instance)'
    )

    cracked_nipples_2_date_onset = models.DateField(
        verbose_name='Approximate date of onset of cracked_nipples (second instance):',
        null=True,
        blank=True
    )

    cracked_nipples_2_type = models.CharField(
        verbose_name='Are the cracked nipples (second instance):',
        max_length=20,
        choices=MASTITIS_TYPE_CHOICES,
        null=True,
        blank=True
    )

    cracked_nipples_2_action = models.ManyToManyField(
        MestitisActions,
        verbose_name='What did the mother do when experiencing cracked nipples (second '
                     'instance)? ',
        max_length=20,
        related_name='cracked_nipples_2_actions',
        blank=True
    )

    cracked_nipples_2_action_other = OtherCharField(
        verbose_name='If Other, specify (second instance)'
    )

    cracked_nipples_3_date_onset = models.DateField(
        verbose_name='Approximate date of onset of cracked_nipples (third instance):',
        null=True,
        blank=True
    )

    cracked_nipples_3_type = models.CharField(
        verbose_name='Are the cracked nipples (third instance):',
        max_length=20,
        choices=MASTITIS_TYPE_CHOICES,
        null=True,
        blank=True
    )

    cracked_nipples_3_action = models.ManyToManyField(
        MestitisActions,
        verbose_name='What did the mother do when experiencing cracked nipples (third '
                     'instance)? ',
        max_length=20,
        related_name='cracked_nipples_3_actions',
        blank=True
    )

    cracked_nipples_3_action_other = OtherCharField(
        verbose_name='If Other, specify (third instance)'
    )

    cracked_nipples_4_date_onset = models.DateField(
        verbose_name='Approximate date of onset of cracked_nipples (fourth instance):',
        null=True,
        blank=True
    )

    cracked_nipples_4_type = models.CharField(
        verbose_name='Are the cracked nipples (fourth instance):',
        max_length=20,
        choices=MASTITIS_TYPE_CHOICES,
        null=True,
        blank=True
    )

    cracked_nipples_4_action = models.ManyToManyField(
        MestitisActions,
        verbose_name='What did the mother do when experiencing cracked nipples (fourth '
                     'instance)? ',
        max_length=20,
        related_name='cracked_nipples_4_actions',
        blank=True
    )

    cracked_nipples_4_action_other = OtherCharField(
        verbose_name='If Other, specify (fourth instance)'
    )

    cracked_nipples_5_date_onset = models.DateField(
        verbose_name='Approximate date of onset of cracked_nipples (fifth instance):',
        null=True,
        blank=True
    )

    cracked_nipples_5_type = models.CharField(
        verbose_name='Are the cracked nipples (fifth instance):',
        max_length=20,
        choices=MASTITIS_TYPE_CHOICES,
        null=True,
        blank=True
    )

    cracked_nipples_5_action = models.ManyToManyField(
        MestitisActions,
        verbose_name='What did the mother do when experiencing cracked nipples (fifth '
                     'instance)? ',
        max_length=20,
        related_name='cracked_nipples_5_actions',
        blank=True
    )

    cracked_nipples_5_action_other = OtherCharField(
        verbose_name='If Other, specify (fifth instance)'
    )

    milk_collected = models.CharField(
        verbose_name='Were you able to collect breast milk today?',
        choices=YES_NO,
        max_length=10,
        null=True,
        blank=True
    )

    not_collected_reasons = models.CharField(
        verbose_name='What was the reason for inability to collect breast milk today',
        choices=NOT_COLLECTED_REASONS_CHOICES,
        max_length=50,
        null=True,
        blank=True
    )

    breast_collected = models.CharField(
        verbose_name='Which breast was the collection from:',
        choices=BREAST_COLLECTED_CHOICES,
        max_length=30,
        null=True,
        blank=True
    )

    milk_collected_volume = models.IntegerField(
        verbose_name='Approximately how much breast milk was collected?(mL)',
        help_text='range from 1mL to 20mL',
        validators=[MinValueValidator(1), MaxValueValidator(4), ],
        null=True,
        blank=True
    )

    last_breastfed = models.DateTimeField(
        verbose_name='What date and time was the infant last breastfed ',
        null=True,
        blank=True
    )

    add_comments = models.TextField(
        verbose_name='Any additional comments ',
        null=True,
        blank=True
    )

    class Meta:
        abstract = True
