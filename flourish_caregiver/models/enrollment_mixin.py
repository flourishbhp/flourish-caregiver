from django import forms
from django.apps import apps as django_apps
from django.db import models
from edc_base.model_validators import date_not_future, datetime_not_future
from edc_base.utils import get_utcnow
from edc_constants.choices import (POS_NEG, POS_NEG_UNTESTED_REFUSAL, YES_NO, YES_NO_NA)
from edc_constants.constants import NO
from edc_protocol.validators import date_not_before_study_start
from edc_protocol.validators import datetime_not_before_study_start

from .eligibility import AntenatalEnrollmentEligibility
from ..helper_classes import EnrollmentHelper


class EnrollmentMixin(models.Model):
    """Base Model for antenatal enrollment"""

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

    current_hiv_status = models.CharField(
        verbose_name="What is your current HIV status?",
        choices=POS_NEG_UNTESTED_REFUSAL,
        max_length=30,
        help_text=("if POS or NEG, ask for documentation."))

    week32_test = models.CharField(
        verbose_name=(
            "Have you tested for HIV before or during this pregnancy?"),
        choices=YES_NO,
        default=NO,
        max_length=3)

    week32_test_date = models.DateField(
        verbose_name="Date of HIV Test",
        validators=[date_not_future, ])

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

    ineligibility = models.TextField(
        verbose_name="Reason not enrolled",
        max_length=350,
        null=True,
        editable=False)

    def save(self, *args, **kwargs):
        enrollment_helper = EnrollmentHelper(instance_antenatal=self)

        self.edd_by_lmp = enrollment_helper.evaluate_edd_by_lmp
        self.ga_lmp_enrollment_wks = enrollment_helper.evaluate_ga_lmp(
            self.get_registration_date())
        self.enrollment_hiv_status = enrollment_helper.enrollment_hiv_status
        self.date_at_32wks = enrollment_helper.date_at_32wks
        if not self.ultrasound:
            self.pending_ultrasound = enrollment_helper.pending
        eligibility_criteria = AntenatalEnrollmentEligibility(
            will_breastfeed=self.will_breastfeed,
            ga_lmp_enrollment_wks=self.ga_lmp_enrollment_wks,
            # enrollment_hiv_status=self.enrollment_hiv_status,
            will_get_arvs=self.will_get_arvs)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        super(EnrollmentMixin, self).save(*args, **kwargs)

    def get_registration_date(self):
        child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')

        child_consents = child_consent_cls.objects.filter(
            subject_identifier=self.child_subject_identifier,
            preg_enroll=True).order_by('consent_datetime')

        if (child_consents and len(set(child_consents.values_list(
                'subject_identifier', flat=True))) == 1):
            child_consent = child_consents[0]
            return child_consent.consent_datetime.date()
        else:
            raise forms.ValidationError(
                'Missing matching Child Subject Consent form, cannot proceed.')

    @property
    def ultrasound(self):
        ultra_sound_cls = django_apps.get_model(
            'flourish_caregiver.ultrasound')
        try:
            ultra_sound_obj = ultra_sound_cls.objects.get(
                maternal_visit__subject_identifier=self.subject_identifier,
                child_subject_identifier=self.child_subject_identifier
            )
        except ultra_sound_cls.DoesNotExist:
            return None
        else:
            return ultra_sound_obj

    class Meta:
        abstract = True
