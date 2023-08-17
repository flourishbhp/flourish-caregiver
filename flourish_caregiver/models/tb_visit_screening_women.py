from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .model_mixins import CrfModelMixin
from ..choices import YES_NO_UNK_DWTA, COUGH_DURATION


class TbVisitScreeningWomen(CrfModelMixin):
    have_cough = models.CharField(
        verbose_name='Do you currently have a cough?',
        choices=YES_NO_UNK_DWTA,
        max_length=30)

    cough_duration = models.CharField(
        verbose_name='What is the duration of your cough?',
        choices=COUGH_DURATION,
        max_length=30,
        blank=True,
        null=True
    )

    cough_intersects_preg = models.CharField(
        verbose_name=('Did you have at least one illness involving cough during pregnancy'
                      ' up to the day of delivery of your baby?'),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30)

    cough_num = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    cough_duration_preg = models.CharField(
        verbose_name='Did any of these coughing illnesses last =>2 weeks?',
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )

    seek_med_help = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving a '
                      'cough?'),
        choices=YES_NO_UNK_DWTA,
        max_length=30,
        null=True,
        blank=True,
    )

    cough_illness = models.CharField(
        verbose_name=('Did you have at least one illness involving cough from after'
                      ' delivery up to yesterday? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30
    )

    cough_illness_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    cough_illness_preg = models.CharField(
        verbose_name='Did any of these coughing illnesses last =>2 weeks?',
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )

    cough_illness_med_help = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving a'
                      ' cough?'),
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )
    fever = models.CharField(
        verbose_name='Do you currently have a fever?',
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30)

    fever_during_preg = models.CharField(
        verbose_name=('Did you have at least one illness involving fever during'
                      ' pregnancy up to the day of delivery of your baby? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30)

    fever_illness_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    fever_illness_preg = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving a'
                      ' fever? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )

    fever_illness_postpartum = models.CharField(
        verbose_name=('Did you have at least one illness involving fever from after'
                      ' delivery up to yesterday? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30
    )

    fever_illness_postpartum_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    fever_illness_postpartum_preg = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses '
                      'involving a fever?'),
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )

    night_sweats = models.CharField(
        verbose_name='Do you currently have night sweats?',
        choices=YES_NO_UNK_DWTA,
        help_text=(' A patient is considered to have night sweats if they have had more '
                   'than two nights of waking up with their night clothing drenched due '
                   'to sweating with a need to change the night clothing'),
        null=True,
        max_length=30)

    night_sweats_during_preg = models.CharField(
        verbose_name=('Did you have at least one illness involving night sweats during '
                      'pregnancy up to the day of delivery of your baby?'),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30
    )

    night_sweats_during_preg_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    night_sweats_during_preg_clinic = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving a'
                      ' night sweats? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )

    night_sweats_postpartum = models.CharField(
        verbose_name=('Did you have at least one illness involving night sweats from '
                      'after delivery up to yesterday? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30
    )

    night_sweats_postpartum_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    night_sweats_postpartum_clinic = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving a '
                      'night sweats?'),
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )

    weight_loss = models.CharField(
        verbose_name='Do you currently have any unexplained weight loss?',
        help_text=('As weight loss after the birth of your baby can be normal, this '
                   'question is referring to any weight loss that does not have an '
                   'explanation.'),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30)

    weight_loss_during_preg = models.CharField(
        verbose_name=('Did you have at least one illness involving unexplained weight '
                      'loss during pregnancy up to the day of delivery of your baby? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30
    )

    weight_loss_during_preg_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    weight_loss_during_preg_clinic = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving '
                      'unexplained weight loss? '),
        null=True,
        blank=True,
        choices=YES_NO_UNK_DWTA,
        max_length=30
    )

    weight_loss_postpartum = models.CharField(
        verbose_name=('Did you have at least one illness involving unexplained weight '
                      'loss from after delivery up to yesterday? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30)

    weight_loss_postpartum_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    weight_loss_postpartum_clinic = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving a '
                      'unexplained weight loss? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )

    cough_blood = models.CharField(
        verbose_name='Have you coughed up blood in the last 2 weeks?',
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30)

    cough_blood_during_preg = models.CharField(
        verbose_name=('Did you have at least one illness involving coughing up blood '
                      'during pregnancy up to the day of delivery of your baby? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30
    )

    cough_blood_during_preg_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    cough_blood_during_preg_clinic = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving '
                      'coughing up blood? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )

    cough_blood_postpartum = models.CharField(
        verbose_name=('Did you have at least one illness involving coughing up blood from'
                      ' after delivery up to yesterday? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30)

    cough_blood_postpartum_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    cough_blood_postpartum_clinic = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving a '
                      'coughing up blood?'),
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )

    enlarged_lymph_nodes = models.CharField(
        verbose_name='Do you currently have enlarged lymph nodes?',
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30)

    enlarged_lymph_nodes_during_preg = models.CharField(
        verbose_name=('Did you have at least one illness involving enlarged lymph nodes '
                      'during pregnancy up to the day of delivery of your baby? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30
    )

    enlarged_lymph_nodes_during_preg_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    enlarged_lymph_nodes_during_preg_clinic = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving '
                      'enlarged lymph nodes? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )

    enlarged_lymph_nodes_postpartum = models.CharField(
        verbose_name=('Did you have at least one illness involving enlarged lymph nodes '
                      'from after delivery up to yesterday? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30)

    enlarged_lymph_nodes_postpartum_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    enlarged_lymph_nodes_postpartum_clinic = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving a '
                      'enlarged lymph nodes?'),
        null=True,
        blank=True,
        choices=YES_NO_UNK_DWTA,
        max_length=30
    )

    unexplained_fatigue = models.CharField(
        verbose_name='Do you currently have unexplained fatigue? ',
        help_text=('As fatigue can be normal after you give birth to your baby, this '
                   'question is referring to fatigue that does not have an explanation.'),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30)

    unexplained_fatigue_during_preg = models.CharField(
        verbose_name=('Did you have at least one illness involving unexplained fatigue '
                      'during pregnancy up to the day of delivery of your baby? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30
    )

    unexplained_fatigue_during_preg_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    unexplained_fatigue_during_preg_clinic = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving '
                      'unexplained fatigue? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )

    unexplained_fatigue_postpartum = models.CharField(
        verbose_name=('Did you have at least one illness involving unexplained fatigue '
                      'from after delivery up to yesterday? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30)

    unexplained_fatigue_postpartum_times = models.IntegerField(
        verbose_name='How many times did this illness happen?',
        help_text='Enter number; range between 1-20.',
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(20)]
    )

    unexplained_fatigue_postpartum_clinic = models.CharField(
        verbose_name=('Did you go to the clinic for this/these illnesses involving a '
                      'unexplained fatigue? '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        blank=True,
        max_length=30
    )

    tb_referral = models.CharField(
        verbose_name=('Were you referred to a TB clinic during pregnancy to 2 months'
                      ' postpartum?  '),
        choices=YES_NO_UNK_DWTA,
        null=True,
        max_length=30)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Screen at 2 months Postpartum'
        verbose_name_plural = 'TB Screen at 2 months Postpartum'
