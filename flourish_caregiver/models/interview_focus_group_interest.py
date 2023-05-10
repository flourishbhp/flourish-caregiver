from django.db import models
from .model_mixins import CrfModelMixin
from ..choices import PREFERENCE_CHOICES, HIV_GROUP_CHOICES, YES_NO_TBD, DISCUSSION_PREF_CHOICES
from edc_constants.choices import YES_NO_UNSURE


class InterviewFocusGroupInterest(CrfModelMixin):
    discussion_pref = models.CharField(
        verbose_name='Would you prefer to participate in a',
        choices=DISCUSSION_PREF_CHOICES,
        max_length=20)

    hiv_group_pref = models.CharField(
        verbose_name='Since you said you would participate in a group discussion,'
                     ' would you prefer the group to be',
        choices=HIV_GROUP_CHOICES,
        max_length=20,
        null=True,
        blank=True)

    infant_feeding = models.CharField(
        verbose_name='Infant feeding discussion preference',
        choices=PREFERENCE_CHOICES,
        max_length=20)

    school_performance = models.CharField(
        verbose_name="Child's school performance discussion preference",
        choices=PREFERENCE_CHOICES,
        max_length=20)

    adult_mental_health = models.CharField(
        verbose_name='Adult mental health discussion preference',
        choices=PREFERENCE_CHOICES,
        max_length=20)

    child_mental_health = models.CharField(
        verbose_name='Child mental health discussion preference',
        choices=PREFERENCE_CHOICES,
        max_length=20)

    sexual_health = models.CharField(
        verbose_name='Sexual reproductive health discussion preference',
        choices=PREFERENCE_CHOICES,
        max_length=20)

    hiv_topics = models.CharField(
        verbose_name='HIV-related topics discussion preference',
        choices=PREFERENCE_CHOICES,
        max_length=20)

    food_insecurity = models.CharField(
        verbose_name='Food insecurity discussion preference',
        choices=PREFERENCE_CHOICES,
        max_length=20)

    wellness = models.CharField(
        verbose_name='Wellness and healthy lifestyle discussion preference',
        choices=PREFERENCE_CHOICES,
        max_length=20)

    non_comm_diseases = models.CharField(
        verbose_name='Non-communicable diseases discussion preference',
        choices=PREFERENCE_CHOICES,
        max_length=20)

    social_issues = models.CharField(
        verbose_name='Social/family issues discussion preference',
        choices=PREFERENCE_CHOICES,
        max_length=20)

    covid19 = models.CharField(
        verbose_name='COVID-19 discussion preference',
        choices=PREFERENCE_CHOICES,
        max_length=20)

    vaccines = models.CharField(
        verbose_name='Vaccines discussion preference',
        choices=PREFERENCE_CHOICES,
        max_length=20)

    infant_feeding_group_interest = models.CharField(
        verbose_name='Would you be interested in participating in a group discussion'
                     ' about how you made your decision on how to feed your baby and how'
                     ' satisfied you are with that decision?',
        choices=YES_NO_TBD,
        max_length=20,
        null=True,
        blank=True,
        help_text="Only required for newly enrolled pregnant women"
    )

    same_status_comfort = models.CharField(
        verbose_name='Would you be comfortable discussing your HIV status in a group'
                     ' of women who have the same HIV '
                     'status as you?',
        choices=YES_NO_UNSURE,
        max_length=20,
        null=True,
        blank=True,
        help_text="women who enrolled in pregnancy and are currently in the 1st year postpartum and"
                  " who answered either "
                  "“group discussion” or “either” in Q3 "
    )

    diff_status_comfort = models.CharField(
        verbose_name='Would you be comfortable discussing your HIV status in'
                     ' a group of women where some may have a '
                     'different HIV status than you?',
        choices=YES_NO_UNSURE,
        max_length=20,
        null=True,
        blank=True,
        help_text="Only required for those who responded either “group discussion” or “either”"
    )

    women_discussion_topics = models.TextField(
        verbose_name='Suggested topics for women in FLOURISH study',
        blank=True)

    adolescent_discussion_topics = models.TextField(
        verbose_name='Suggested topics for adolescents in FLOURISH study',
        blank=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Interview and Focus Group Interest CRF'
        verbose_name_plural = 'Interview and Focus Group Interest CRFs'
