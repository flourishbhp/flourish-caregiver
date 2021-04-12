from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .model_mixins import CrfModelMixin


class ObstericalHistory(CrfModelMixin):

    """ A model completed by the user on Obsterical History for ONLY biological
        mothers.
    """

    prev_pregnancies = models.IntegerField(
        verbose_name=('Including the pregnancy of the child in the FLOURISH '
                      'study, how many previous pregnancies for this participant?'),
        validators=[MinValueValidator(1), MaxValueValidator(20), ],
    )

    pregs_24wks_or_more = models.IntegerField(
        verbose_name='Number of pregnancies at least 24 weeks?',
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
    )

    lost_before_24wks = models.IntegerField(
        verbose_name='Number of pregnancies lost before 24 weeks gestation',
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
    )

    lost_after_24wks = models.IntegerField(
        verbose_name='Number of pregnancies lost at or after 24 weeks'
        ' gestation ',
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
    )

    live_children = models.IntegerField(
        verbose_name='How many living children does the participant have?',
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
    )

    children_died_b4_5yrs = models.IntegerField(
        verbose_name='How many of the participant\'s children died after '
        'birth before 5 years of age? ',
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
    )

    children_deliv_before_37wks = models.IntegerField(
        verbose_name='Number of previous pregnancies delivered at < 37'
        ' weeks GA?',
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
    )

    children_deliv_aftr_37wks = models.IntegerField(
        verbose_name='Number of previous pregnancies delivered at >= 37'
        ' weeks GA?',
        validators=[MinValueValidator(0), MaxValueValidator(20), ],
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Obsterical History'
        verbose_name_plural = 'Obsterical History'
