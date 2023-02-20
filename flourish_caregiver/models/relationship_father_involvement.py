from django.db import models
from django_crypto_fields.fields import EncryptedCharField
from edc_base.model_validators import CellNumber
from edc_protocol.validators import datetime_not_before_study_start
from edc_base.model_validators import datetime_not_future
from edc_base.utils import get_utcnow
from edc_base.model_fields.custom_fields import OtherCharField

from django.core.validators import MinValueValidator, MaxValueValidator
from edc_constants.choices import YES_NO

from ..choices import (YES_NO_PNTA, YES_NO_PNTA_NA, YES_NO_PNTA_UNKNOWN,
                       HIV_STATUS_DISCUSSION, PARTNERS_SUPPORT,
                       CHOICE_FREQUENCY, HAPPINESS_CHOICES, FATHER_VISITS,
                       FUTURE_OF_RELATIONSHIP, FATHERS_FINANCIAL_SUPPORT, HOUSEHOLD_MEMBER)
from .list_models import HouseholdMember
from .model_mixins import CrfModelMixin


class RelationshipFatherInvolvement(CrfModelMixin):
    """A CRF to be completed by biological mothers living with HIV,
    at enrollment, annual (every 4th quarterly call), and follow-up
    """

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, datetime_not_before_study_start], )

    partner_present = models.CharField(
        verbose_name="Do you currently have a partner? ",
        choices=YES_NO_PNTA,
        max_length=25)

    why_partner_absent = models.TextField(
        verbose_name='Why not',
        max_length=250,
        blank=True,
        null=True)

    is_partner_the_father = models.CharField(
        verbose_name='Is the partner you are currently with also the'
        ' father of this child enrolled in FLOURISH?',
        choices=YES_NO_PNTA_UNKNOWN,
        max_length=25,
        blank=True,
        null=True)

    duration_with_partner = models.FloatField(
        verbose_name='How long have you been with your current partner?',
        help_text='(Years).(Months), For example 1.5 year is equavalent to 1 years 6 months',
        default=0,
        validators=[MinValueValidator(0)],
        blank=True,
        null=True)

    partner_age_in_years = models.PositiveIntegerField(
        verbose_name='How old is your partner?',
        help_text='(Years)',
        blank=True,
        null=True)

    living_with_partner = models.CharField(
        verbose_name="Are you currently living together? ",
        choices=YES_NO_PNTA,
        max_length=4,
        blank=True,
        null=True)

    why_not_living_with_partner = models.TextField(
        verbose_name='Why not',
        max_length=250,
        blank=True,
        null=True)

    disclosure_to_partner = models.CharField(
        verbose_name="Have you disclosed your HIV status to your partner",
        choices=YES_NO_PNTA_NA,
        max_length=25, )

    discussion_with_partner = models.CharField(
        verbose_name="How easy or difficult is it to  discuss your HIV status  with your partner?",
        choices=HIV_STATUS_DISCUSSION,
        max_length=17, )

    disclose_status = models.CharField(
        verbose_name='Do you plan to disclosure your HIV status to'
        ' your partner at some time in the future',
        choices=YES_NO_PNTA_NA,
        max_length=23, )

    partners_support = models.CharField(
        verbose_name="In general, how supportive is your partner?",
        choices=PARTNERS_SUPPORT,
        max_length=20,
        blank=True,
        null=True)

    ever_separated = models.CharField(
        verbose_name="Have you and your partner ever separated before?",
        choices=YES_NO_PNTA,
        max_length=25,
        blank=True,
        null=True)

    times_separated = models.TextField(
        verbose_name="How many times have you separated from your partner?",
        max_length=250,
        blank=True,
        null=True)

    separation_consideration = models.CharField(
        verbose_name="How often have you considered divorce, separation, or terminating your relationship?",
        choices=CHOICE_FREQUENCY,
        max_length=20,
        blank=True,
        null=True)

    leave_after_fight = models.CharField(
        verbose_name="How often do you or your partner leave the house after a fight?",
        choices=CHOICE_FREQUENCY,
        max_length=20,
        blank=True,
        null=True)

    relationship_progression = models.CharField(
        verbose_name="In general, how often do you think that things between you and your partner are going well?",
        choices=CHOICE_FREQUENCY,
        max_length=20,
        blank=True,
        null=True)

    confide_in_partner = models.CharField(
        verbose_name="Do you confide in your partner?",
        choices=CHOICE_FREQUENCY,
        max_length=20,
        blank=True,
        null=True)

    relationship_regret = models.CharField(
        verbose_name="Do you ever regret that you entered a relationship with your partner?",
        choices=CHOICE_FREQUENCY,
        max_length=20,
        blank=True,
        null=True)

    quarrel_frequency = models.CharField(
        verbose_name="How often do you and your partner quarrel?",
        choices=CHOICE_FREQUENCY,
        max_length=20,
        blank=True,
        null=True)

    bothering_partner = models.CharField(
        verbose_name="How often do you and your partner bother each other?",
        choices=CHOICE_FREQUENCY,
        max_length=20,
        blank=True,
        null=True)

    kissing_partner = models.CharField(
        verbose_name="How often do you and your partner kiss each other? ",
        choices=CHOICE_FREQUENCY,
        max_length=20,
        blank=True,
        null=True)

    engage_in_interests = models.CharField(
        verbose_name="Do you and your partner engage in shared interests together?",
        choices=CHOICE_FREQUENCY,
        max_length=20,
        blank=True,
        null=True)

    happiness_in_relationship = models.CharField(
        verbose_name='All things considered, how happy are you in your relationship?',
        choices=HAPPINESS_CHOICES,
        max_length=20,
        blank=True,
        null=True)

    future_relationship = models.CharField(
        verbose_name='Which of the following statements best describes how you'
        ' feel about the future of your relationship?',
        choices=FUTURE_OF_RELATIONSHIP,
        max_length=20,
        help_text='(Partnership success can be defined as staying together.)',
        blank=True,
        null=True)

    biological_father_alive = models.CharField(
        verbose_name='Is the biological father of this child alive',
        choices=YES_NO_PNTA,
        max_length=4,)

    father_child_contact = models.CharField(
        verbose_name='How often does the biological father have contact '
        '(home visits, phone calls, meeting up at another place) with your child? ',
        choices=FATHER_VISITS,
        max_length=30,)

    fathers_financial_support = models.CharField(
        verbose_name='How supportive is the father in financially supporting the child?',
        choices=FATHERS_FINANCIAL_SUPPORT,
        max_length=20,)

    child_left_alone = models.PositiveIntegerField(
        default=0,
        verbose_name='How many days in the last week did you have to'
        ' leave your child alone at home without an adult?',
        help_text='Range from (0-7)',
        validators=[MinValueValidator(0), MaxValueValidator(7), ],)

    read_books = models.ManyToManyField(
        HouseholdMember,
        related_name='read_books',
        verbose_name='Read books or looked at picture books with your child', )

    read_books_other = OtherCharField()

    told_stories = models.ManyToManyField(
        HouseholdMember,
        related_name='told_stories',
        verbose_name='Told stories to your child', )

    told_stories_other = OtherCharField()

    sang_songs = models.ManyToManyField(
        HouseholdMember,
        related_name='sang_songs',
        verbose_name='Sang songs to or with your child, including lullabies', )

    sang_songs_other = OtherCharField()

    took_child_outside = models.ManyToManyField(
        HouseholdMember,
        related_name='took_child_outside',
        verbose_name='Took your child outside the home', )

    took_child_outside_other = OtherCharField()

    played_with_child = models.ManyToManyField(
        HouseholdMember,
        related_name='played_with_child',
        verbose_name='Played with your child', )

    played_with_child_other = OtherCharField()

    named_with_child = models.ManyToManyField(
        HouseholdMember,
        related_name='named_with_child',
        verbose_name='Named, counted, or drew things with or for your child', )

    named_with_child_other = OtherCharField()

    interview_participation = models.CharField(
        verbose_name='Would you be willing to participate in an interview'
        ' to teach us more about caregiving?',
        choices=YES_NO,
        max_length=3)

    contact_info = models.CharField(
        verbose_name=('Would you be willing to provide us contact information so we'
                      ' can invite your partner or ex-partner (who is supporting '
                      'the caregiving of the FLOURISH child) to an interview about caregiving?'),
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    partner_cell = EncryptedCharField(
        verbose_name="Cell number",
        max_length=8,
        validators=[CellNumber, ],
        blank=True,
        null=True)

    conunselling_referral = models.CharField(
        verbose_name=('According to the clinician completing this form, does this '
                      'participant need a referral for counselling?'),
        choices=YES_NO,
        max_length=3,
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Relationship and Father Involvement'
        verbose_name_plural = 'Relationship and Father Involvement'
