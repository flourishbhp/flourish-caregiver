from django.db import models
from . import CrfModelMixin
from edc_constants.choices import YES_NO


class CageAidFieldsMixin(models.Model):

    alcohol_drugs = models.CharField(
        verbose_name='Do you partake in drinking alcohol or using nonmedicinal drugs?',
        choices=YES_NO,
        max_length=10,
    )

    cut_down = models.CharField(
        verbose_name='Have you ever felt the need to cut down on your drinking or drug use?',
        choices=YES_NO,
        max_length=10,
        null=True,
        blank=True,
        default=None
    )
    people_reaction = models.CharField(
        verbose_name='Have people annoyed you by criticizing your drinking or drug use?',
        choices=YES_NO,
        max_length=10,
        null=True,
        blank=True,
        default=None
    )
    guilt = models.CharField(
        verbose_name='Have you ever felt guilty about drinking or drug use?',
        choices=YES_NO,
        max_length=10,
        null=True,
        blank=True,
        default=None
    )
    eye_opener = models.CharField(
        verbose_name=('Have you ever felt you needed a drink or used drugs first '
                      'thing in the morning to steady your nerves or to get rid of a hangover (Eye-Opener)?'),
        choices=YES_NO,
        max_length=10,
        null=True,
        blank=True,
        default=None
    )

    class Meta:
        abstract = True
