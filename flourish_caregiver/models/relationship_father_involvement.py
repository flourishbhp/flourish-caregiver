from django.db import models
from .model_mixins import CrfModelMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_base.model_validators import datetime_not_future
from edc_base.utils import get_utcnow

from django.core.validators import MinValueValidator, MaxValueValidator
from edc_base.model_fields import OtherCharField
from edc_constants.constants import NOT_APPLICABLE
from edc_constants.choices import YES_NO, YES_NO_NA
from ..choices import (YES_NO_PNTA,YES_NO_PNTA_UNKNOWN,
                       HIV_STATUS_DISCUSSION,PARTNERS_SUPPORT,
                       CHOICE_FREQUENCY,HAPPINESS_CHOICES,FATHER_VISITS,
                       FATHERS_FINANCIAL_SUPPORT,HOUSEHOLD_MEMBER)

from django_crypto_fields.fields import EncryptedCharField

class RelationshipFatherInvolvement(CrfModelMixin):
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
    
    Q3-duration_with_partner-help_text='(Months,Years)'
    duration_with_partner_months = models.PositiveIntegerField(
        verbose_name='How long have you been with your current partner?',
        help_text='(Months)',)
    
    duration_with_partner_years = models.PositiveIntegerField(
        default=0,
        verbose_name='Years',
        help_text='(Years)',)
    
    
    
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
    happiness_in_relationship = models.CharField(
        verbose_name='All things considered, how happy are you in your relationship?',
        choices=HAPPINESS_CHOICES,
        max_length=20,
    )
    
    Q22
    future_relationship = models.CharField(
        verbose_name='Which of the following statements best describes how you'
        'feel about the future of your relationship?',
        choices=HAPPINESS_CHOICES,
        max_length=20,
        help_text='(Partnership success can be defined as staying together.)',
    )
    
    # section 3 questions
    
    Q23
    father_child_contact = models.CharField(
        verbose_name='How often does the biologic father have contact '
        '(home visits, phone calls, meeting up at another place) with your child? ',
        choices=FATHER_VISITS,
        max_length=30,
    )
    
    Q24
    fathers_financial_support = models.CharField(
        verbose_name='How supportive is the father in financially supporting the child?',
        choices=FATHERS_FINANCIAL_SUPPORT,
        max_length=20,
    )
    
    Q25
    child_left_alone = models.PositiveIntegerField(
        default=0,
        verbose_name='How many days in the last week did you have to'
        'leave your child alone at home without an adult?',
        help_text='Range from (0-7)',
        validators=[MinValueValidator(0), MaxValueValidator(7), ],
       )
    
    Q26
    read_books = models.CharField(
        verbose_name='Read books or looked at picture books with your child',
        choices=HOUSEHOLD_MEMBER,
        max_length=10,
    )
    
    Q27
    told_stories = models.CharField(
        verbose_name='Told stories to your child',
        choices=HOUSEHOLD_MEMBER,
        max_length=10,
    )
    
    Q28
    sang_songs = models.CharField(
        verbose_name='Sang songs to or with your child, including lullabies',
        choices=HOUSEHOLD_MEMBER,
        max_length=10,
    )
    
    Q29
    took_child_outside = models.CharField(
        verbose_name='Took your child outside the home',
        choices=HOUSEHOLD_MEMBER,
        max_length=10,
    )
    
    Q30
    played_with_child = models.CharField(
        verbose_name='Played with your child',
        choices=HOUSEHOLD_MEMBER,
        max_length=10,
    )
    
    Q31
    named_with_child = models.CharField(
        verbose_name='Named, counted, or drew things with or for your child',
        choices=HOUSEHOLD_MEMBER,
        max_length=10,
    )
    
    # Stem question for Q25 – Q30: In the past 3 days, did you or any household member aged 15 or over engage in any of the following activities with the child
    
    # SECTION 4
    Q32
    interview_participation = models.CharField(
        verbose_name='Would you be willing to participate in an interview'
        'to teach us more about caregiving?',
        choices=YES_NO,
        max_length=3
    )
    
    Q33
    contact_info = models.CharField(
        verbose_name='Would you be willing to provide us contact information so we'
        'can invite your partner to an interview about caregiving?',
        choices=YES_NO,
        max_length=3
    )
    Q33 -contact_info
    
    
