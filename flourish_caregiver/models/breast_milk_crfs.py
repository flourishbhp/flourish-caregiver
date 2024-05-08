from django.db import models
from django.db.models import PROTECT
from edc_base.model_fields import OtherCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future, datetime_not_future
from .list_models import CrackedNipplesActions, MastitisActions
from .model_mixins.breast_milk_field_mixin import \
    BreastMilkFieldsMixin
from ..choices import MASTITIS_TYPE_CHOICES


class BreastMilkBirth(BreastMilkFieldsMixin, models.Model):
    class Meta:
        proxy = True
        app_label = 'flourish_caregiver'
        verbose_name = "Breast Milk Collection CRF at Birth Visit"
        verbose_name_plural = "Breast Milk Collection CRF at Birth Visit"


class BreastMilk6Months(BreastMilkFieldsMixin, models.Model):
    class Meta:
        proxy = True
        app_label = 'flourish_caregiver'
        verbose_name = "Breast Milk Collection CRF at 6-Month "
        verbose_name_plural = "Breast Milk Collection CRF at 6-Month "


class MastitisInline(BaseUuidModel):
    breast_milk_crf = models.ForeignKey(
        BreastMilkFieldsMixin, on_delete=PROTECT)

    mastitis_date_onset = models.DateField(
        verbose_name='Approximate date of onset of mastitis: ',
        null=True,
        validators=[date_not_future, ],
    )

    mastitis_type = models.CharField(
        verbose_name='Is the mastitis:',
        max_length=20,
        choices=MASTITIS_TYPE_CHOICES,
        null=True,
    )

    mastitis_action = models.ManyToManyField(
        MastitisActions,
        verbose_name='What did the mother do? ',
        max_length=20,
        related_name='mastitis_actions',
    )

    mastitis_action_other = OtherCharField(
        verbose_name='If Other, specify'
    )

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = "Mastitis Inline"
        verbose_name_plural = "Mastitis Inlines"


class CrackedNipplesInline(BaseUuidModel):
    breast_milk_crf = models.ForeignKey(
        BreastMilkFieldsMixin, on_delete=PROTECT)

    cracked_nipples_date_onset = models.DateField(
        verbose_name='Approximate date of onset of cracked nipples: ',
        null=True,
        validators=[date_not_future, ],
    )

    cracked_nipples_type = models.CharField(
        verbose_name='Are the cracked nipples:',
        max_length=20,
        choices=MASTITIS_TYPE_CHOICES,
        null=True,
    )

    cracked_nipples_action = models.ManyToManyField(
        CrackedNipplesActions,
        verbose_name='What did the mother do when experiencing cracked nipples? ',
        max_length=20,
        related_name='cracked_nipples_actions',
    )

    cracked_nipples_action_other = OtherCharField(
        verbose_name='If Other, specify'
    )

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = "Cracked Nipples Inline"
        verbose_name_plural = "Cracked Nipples Inlines"
