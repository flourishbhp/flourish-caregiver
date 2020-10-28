from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from django.db import models
from edc_base.model_validators import datetime_not_future, date_not_future
from edc_base.utils import get_utcnow
from edc_constants.choices import (
    POS_NEG_UNTESTED_REFUSAL, YES_NO_NA, POS_NEG, YES_NO)
from edc_constants.constants import NO, YES, POS, NEG
from edc_protocol.validators import date_not_before_study_start
from edc_protocol.validators import datetime_not_before_study_start

from ..helper_classes import EnrollmentHelper


class EnrollmentMixin(models.Model):

    """Base Model for antenal enrollment"""

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        default=get_utcnow,
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    enrollment_hiv_status = models.CharField(
        max_length=15,
        null=True,
        editable=False,
        help_text='Auto-filled by enrollment helper')

    date_at_32wks = models.DateField(
        null=True,
        editable=False,
        help_text='Auto-filled by enrollment helper')

    is_eligible = models.BooleanField(
        editable=False)

    pending_ultrasound = models.BooleanField(
        editable=False)

    is_diabetic = models.CharField(
        verbose_name='Are you diabetic?',
        choices=YES_NO,
        max_length=3)

    will_breastfeed = models.CharField(
        verbose_name='Do you intent to breast-feed your child for 6 months?',
        choices=YES_NO,
        help_text='INELIGIBLE if NO',
        max_length=3)

    will_remain_onstudy = models.CharField(
        verbose_name="Are you willing to remain in the study for the"
        " child's first five years of life",
        choices=YES_NO,
        help_text='INELIGIBLE if NO',
        max_length=3)

    current_hiv_status = models.CharField(
        verbose_name="What is your current HIV status?",
        choices=POS_NEG_UNTESTED_REFUSAL,
        max_length=30,
        help_text=("if POS or NEG, ask for documentation."))

    evidence_hiv_status = models.CharField(
        verbose_name="(Interviewer) Have you seen evidence of the HIV result?",
        max_length=15,
        null=True,
        blank=False,
        choices=YES_NO_NA,
        help_text=(
            "evidence = clinic and/or IDCC records. check regimes/drugs. "
            "If NO, more criteria required."))

    week32_test = models.CharField(
        verbose_name=(
            "Have you tested for HIV before or during this pregnancy?"),
        choices=YES_NO,
        default=NO,
        max_length=3)

    week32_test_date = models.DateField(
        verbose_name="Date of HIV Test",
        validators=[date_not_future, ])

    week32_result = models.CharField(
        verbose_name="What was your result?",
        choices=POS_NEG,
        max_length=15,
        null=True,
        blank=True)

    evidence_32wk_hiv_status = models.CharField(
        verbose_name=(
            "(Interviewer) Have you seen evidence of the result from "
            "HIV test on or before this pregnancy?"),
        max_length=15,
        null=True,
        blank=False,
        choices=YES_NO_NA,
        help_text=(
            "evidence = clinic and/or IDCC records. check regimes/drugs."))

    will_get_arvs = models.CharField(
        verbose_name=("(Interviewer) If HIV+ve, do records show that "
                      "participant is taking, is prescribed,"
                      "or will be prescribed ARVs (if newly diagnosed) "
                      "during pregnancy?"),
        choices=YES_NO_NA,
        null=True,
        blank=False,
        max_length=15,
        help_text="If found POS by RAPID TEST. Then answer YES")

    rapid_test_done = models.CharField(
        verbose_name="Was a rapid test processed?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        max_length=15,
        help_text=(
            "Remember, rapid test is for NEG, UNTESTED, UNKNOWN and Don\'t"
            " want to answer."))

    rapid_test_date = models.DateField(
        verbose_name="Date of rapid test",
        null=True,
        validators=[
            date_not_before_study_start,
            date_not_future],
        blank=True)

    rapid_test_result = models.CharField(
        verbose_name="What is the rapid test result?",
        choices=POS_NEG,
        max_length=15,
        null=True,
        blank=True)

    unenrolled = models.TextField(
        verbose_name="Reason not enrolled",
        max_length=350,
        null=True,
        editable=False)

    def save(self, *args, **kwargs):
        enrollment_helper = EnrollmentHelper(instance_antenatal=self)
#      if not enrollment_helper.validate_rapid_test():
#        raise ValidationError('Ensure a rapid test id done for this subject.')
        self.edd_by_lmp = enrollment_helper.evaluate_edd_by_lmp
        self.ga_lmp_enrollment_wks = enrollment_helper.evaluate_ga_lmp(
            self.get_registration_date())
        self.enrollment_hiv_status = enrollment_helper.enrollment_hiv_status
        self.date_at_32wks = enrollment_helper.date_at_32wks

        self.is_eligible = self.antenatal_criteria(enrollment_helper)
        self.unenrolled = self.unenrolled_error_messages()
        super(EnrollmentMixin, self).save(*args, **kwargs)

    def antenatal_criteria(self, enrollment_helper):
        """Returns True if basic criteria is met for enrollment.
        """
        if self.pending_ultrasound:
            basic_criteria = False
        else:
            lmp_to_use = self.ga_lmp_enrollment_wks
            basic_criteria = (lmp_to_use >= 21 and lmp_to_use <= 29 and
                              enrollment_helper.no_chronic_conditions() and
                              self.will_breastfeed == YES and
                              self.will_remain_onstudy == YES)
        if (basic_criteria and self.enrollment_hiv_status == POS and
                self.will_get_arvs == YES):
            return True
        elif basic_criteria and self.enrollment_hiv_status == NEG:
            return True
        else:
            return False

    def get_registration_date(self):
        consent_cls = django_apps.get_model('flourish_maternal.subjectconsent')
        try:
            subject_consent = consent_cls.objects.filter(
                subject_identifier=self.subject_identifier).order_by(
                    'consent_datetime')[0]
        except Exception as e:
            raise ValidationError(e)
        else:
            return subject_consent.consent_datetime.date()

    @property
    def ultrasound(self):
        MaternalUltraSoundInitial = django_apps.get_model(
            'flourish_maternal.maternalultrasoundinitial')
        try:
            maternal_ultra_sount_initial = MaternalUltraSoundInitial.objects.get(
                maternal_visit__subject_identifier=self.subject_identifier)
        except MaternalUltraSoundInitial.DoesNotExist:
            return None
        else:
            return maternal_ultra_sount_initial

    class Meta:
        abstract = True
