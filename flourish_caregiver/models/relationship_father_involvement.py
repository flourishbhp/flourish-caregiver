from django.db import models
from .model_mixins import CrfModelMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_base.model_validators import datetime_not_future
from edc_base.utils import get_utcnow

from edc_base.model_fields import OtherCharField
from edc_constants.constants import NOT_APPLICABLE
from edc_constants.choices import YES_NO, YES_NO_NA
from ..choices import (YES_NO_PNTA,YES_NO_PNTA_UNKNOWN,
                       HIV_STATUS_DISCUSSION,PARTNERS_SUPPORT,
                       CHOICE_FREQUENCY,HAPPINESS_CHOICES)


class RelationshipFatherInvolment(CrfModelMixin):
    """A CRF to be completed by biological mothers living with HIV,
    at enrollment, annual (every 4th quarterly call), and follow-up
    
    
    """
    # section 1 questions
    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, datetime_not_before_study_start], )
    
    Q1-partner_present
    partner_present = models.CharField(
        verbose_name="Do you currently have a partner? ",
        choices=YES_NO,
        max_length=3
    )
    Q2-is_partner_the_father
    is_partner_the_father = models.CharField(
        verbose_name='Is the partner you are currently with also the' 
        'father of this child enrolled in FLOURISH?',
        choices=YES_NO_PNTA_UNKNOWN,
        max_length=25
    )
    
    # Q3-duration_with_partner -help_text='(Months,Years)'
    
    
    Q4-partner_age
    partner_age_in_years = models.PositiveIntegerField(
        verbose_name='How old is your partner?',
        help_text='(Years)',)
    
    Q5-living_with_partner
    living_with_partner = models.CharField(
        verbose_name="Are you currently living together? ",
        choices=YES_NO,
        max_length=3
    )
    
    not_living_with_partner = models.TextField(
        verbose_name='Why not',
        max_length=250,
        blank=True,
        null=True)
    
    
    Q6-discloure_to_partner
    discloure_to_partner = models.CharField(
        verbose_name="Have you disclosed your HIV status to your partner",
        choices=YES_NO_PNTA,
        max_length=25
    )
    
    
    Q7-discussion_with_partner
    discussion_with_partner = models.CharField(
        verbose_name="How easy or difficult is it to  discuss your HIV status  with your partner?",
        choices=HIV_STATUS_DISCUSSION,
        max_length=17
    )
    
    Q8-disclose_status
    disclose_status = models.CharField(
        verbose_name='Do you plan to disclosure your HIV status to'
        'your partner at some time in the future',
        choices=YES_NO_PNTA,
        max_length=23
    )
    
    Q9-partners_support
    partners_support = models.CharField(
        verbose_name="In general, how supportive is your partner?",
        choices=PARTNERS_SUPPORT,
        max_length=20
    )
    
    Q10-ever_separated
    ever_separated = models.CharField(
        verbose_name="Have you and your partner every separated before?",
        choices=YES_NO,
        max_length=3
    )
    
    Q11-times_separated
    times_separated = models.TextField(
        verbose_name="How many times have you separated from your partner?",
        max_length=250,
        blank=True,
        null=True)
    
    
    # section 2 questions
    Q12
    separation_consideration = models.CharField(
        verbose_name="How often have you considered divorce, separation, or terminating your relationship?",
        choices=CHOICE_FREQUENCY,
        max_length=20
    )
    
    Q13
    after_fight = models.CharField(
        verbose_name="How often do you or your partner leave the house after a fight?",
        choices=CHOICE_FREQUENCY,
        max_length=20
    )
    
    Q14
    relationship_progression = models.CharField(
        verbose_name="In general, how often do you think that things between you and your partner are going well?",
        choices=CHOICE_FREQUENCY,
        max_length=20
    )
    Q15
    confide_in_partner = models.CharField(
        verbose_name="Do you confide in your partner?",
        choices=CHOICE_FREQUENCY,
        max_length=20
    )
    Q16
    relationship_regret = models.CharField(
        verbose_name="Do you ever regret that you entered a relationship with your partner?",
        choices=CHOICE_FREQUENCY,
        max_length=20
    )
    Q17
    quarrel_frequency = models.CharField(
        verbose_name="How often do you and your partner quarrel?",
        choices=CHOICE_FREQUENCY,
        max_length=20
    )
    Q18
    bothering_partner = models.CharField(
        verbose_name="How often do you and your partner bother each other?",
        choices=CHOICE_FREQUENCY,
        max_length=20
    )
    Q19
    kissing_partner = models.CharField(
        verbose_name="How often do you and your partner kiss each other? ",
        choices=CHOICE_FREQUENCY,
        max_length=20
    )
    Q20
    engage_in_interests = models.CharField(
        verbose_name="Do you and your partner engage in shared interests together?",
        choices=CHOICE_FREQUENCY,
        max_length=20
    )
    Q21
    engage_in_interests = models.CharField(
        verbose_name='Which of the following statements best describes how you'
        'feel about the future of your relationship?',
        choices=HAPPINESS_CHOICES,
        max_length=20,
    )
    
    Q22
    engage_in_interests = models.CharField(
        verbose_name='Which of the following statements best describes how you'
        'feel about the future of your relationship?',
        choices=HAPPINESS_CHOICES,
        max_length=20,
        help_text='(Partnership success can be defined as staying together.)',
    )
    
    # section 3 questions