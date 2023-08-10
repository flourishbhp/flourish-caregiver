from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import date_not_before_study_start

from .enrollment_mixin import EnrollmentMixin
from .maternal_delivery import MaternalDelivery
from .ultrasound import UltraSound


class AntenatalEnrollment(UniqueSubjectIdentifierFieldMixin,
                          EnrollmentMixin, BaseUuidModel):
    knows_lmp = models.CharField(
        verbose_name="Does the mother know the approximate date "
                     "of the first day her last menstrual period?",
        choices=YES_NO,
        help_text='LMP',
        max_length=3)

    last_period_date = models.DateField(
        verbose_name="What is the approximate date of the first day of "
                     "the mother’s last menstrual period",
        validators=[date_not_future, ],
        null=True,
        blank=True,
        help_text='LMP')

    ga_lmp_enrollment_wks = models.IntegerField(
        verbose_name="GA at enrollment.",
        help_text=" (weeks of gestation at enrollment, LMP). Eligible if"
                  " >16 and <30 weeks GA",
        null=True,
        blank=True,)

    ga_lmp_anc_wks = models.IntegerField(
        verbose_name="What is the mother's gestational age according to"
                     " ANC records (or from midwife if LMP is not known)?",
        validators=[MinValueValidator(1), MaxValueValidator(40)],
        null=True,
        blank=True,
        help_text=" (weeks of gestation at enrollment, ANC)",)

    edd_by_lmp = models.DateField(
        verbose_name="Estimated date of delivery by lmp",
        validators=[
            date_not_before_study_start],
        null=True,
        blank=True)

    @property
    def real_time_ga(self):
        """
        Changing, GA in realtime

        Returns:
            str: returns a message or calculate GA
        """
        try:

            ultrasound = UltraSound.objects.get(
                maternal_visit__subject_identifier=self.subject_identifier)
        except UltraSound.DoesNotExist:
            result = "Fill The Ultrasound CRF First"
        else:
            try:

                maternal_delivery = MaternalDelivery.objects.get(
                    subject_identifier=self.subject_identifier)
            except MaternalDelivery.DoesNotExist:
                # if child is not yet delivered
                today = get_utcnow()
                result = ultrasound.ga_confirmed + ((today - ultrasound.report_datetime).days / 7)
            else:
                # if child is already delivered stop changing GA
                delivery_date = maternal_delivery.delivery_datetime

                result = ultrasound.ga_confirmed + ((delivery_date - ultrasound.report_datetime).days / 7)

        return round(result, 1)

    history = HistoricalRecords()

    def __str__(self):
        return f'antenatal: {self.subject_identifier}'

    # def unenrolled_error_messages(self):
    # """Returns a tuple (True, None) if mother is eligible otherwise
    # (False, unenrolled_error_message) where error message is the reason
    # enrollment failed."""
    #
    # unenrolled_error_message = []
    # if self.will_breastfeed == NO:
    # unenrolled_error_message.append('will not breastfeed')
    # if self.will_get_arvs == NO:
    # unenrolled_error_message.append(
    # 'Will not get ARVs on this pregnancy.')
    # if self.rapid_test_done == NO:
    # unenrolled_error_message.append('rapid test not done')
    # if (self.ga_lmp_enrollment_wks and
    # (self.ga_lmp_enrollment_wks < 22 or
    # self.ga_lmp_enrollment_wks > 28)):
    # unenrolled_error_message.append('gestation not 22 to 28wks')
    #
    # if self.ultrasound and not self.ultrasound.pass_antenatal_enrollment:
    # unenrolled_error_message.append('Pregnancy is not a singleton.')
    # return unenrolled_error_message

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Maternal Antenatal Enrollment'
        verbose_name_plural = 'Maternal Antenatal Enrollment'
