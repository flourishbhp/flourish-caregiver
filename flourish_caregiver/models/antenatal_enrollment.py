from django.apps import apps as django_apps
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import date_not_before_study_start

from .enrollment_mixin import EnrollmentMixin
from .maternal_delivery import MaternalDelivery
from .ultrasound import UltraSound


class AntenatalModelManager(models.Manager):
    use_in_migrations = True


class AntenatalEnrollment(NonUniqueSubjectIdentifierFieldMixin,
                          EnrollmentMixin, BaseUuidModel):
    child_subject_identifier = models.CharField(
        verbose_name="Associated Child Identifier",
        max_length=50,
        unique=True)

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
        blank=True, )

    ga_lmp_anc_wks = models.IntegerField(
        verbose_name="What is the mother's gestational age according to"
                     " ANC records (or from midwife if LMP is not known)?",
        validators=[MinValueValidator(1), MaxValueValidator(40)],
        null=True,
        blank=True,
        help_text=" (weeks of gestation at enrollment, ANC)", )

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
                child_subject_identifier=self.child_subject_identifier,
                maternal_visit__subject_identifier=self.subject_identifier)
        except UltraSound.DoesNotExist:
            return "Fill The Ultrasound CRF First"
        else:
            try:

                maternal_delivery = MaternalDelivery.objects.get(
                    child_subject_identifier=self.child_subject_identifier,
                    subject_identifier=self.subject_identifier)
            except MaternalDelivery.DoesNotExist:
                # if child is not yet delivered
                today = self.caregiver_offstudy_dt or get_utcnow().date()

                result = self.calculate_ga_weeks(ultrasound, reference_dt=today)
            else:
                # if child is already delivered stop changing GA
                delivery_date = maternal_delivery.delivery_datetime.date()

                result = self.calculate_ga_weeks(ultrasound, reference_dt=delivery_date)

        return round(result, 1)

    def calculate_ga_weeks(self, ultrasound=None, reference_dt=get_utcnow().date()):
        """ Calculate gestational age by weeks, if EDD confirmed by lmp = 0: use lmp
            to determine GA weeks, elif EDD confirmed by ultrasound = 1: use ga by
            ultrasound to determine GA weeks.
            @param ultrasound: Ultrasound object
            @param reference_dt: delivery date if delivered else current date for
                                 current GA otherwise off-study date for GA at off-study.
        """
        ga_weeks = None
        confirmation_method = getattr(ultrasound, 'ga_confrimation_method', None)
        ga_by_ultrasound_wks = getattr(ultrasound, 'ga_by_ultrasound_wks', None)
        ga_by_ultrasound_days = getattr(ultrasound, 'ga_by_ultrasound_days', None)
        if confirmation_method == '0':
            try:
                ga_weeks = (reference_dt - self.last_period_date).days / 7
            except TypeError:
                pass
        elif confirmation_method == '1':
            try:
                us_days = (ga_by_ultrasound_wks * 7) + ga_by_ultrasound_days
                us_dd = reference_dt - ultrasound.report_datetime.date()
                ga_weeks = (us_dd.days + us_days) / 7
            except TypeError:
                pass
        return ga_weeks

    objects = AntenatalModelManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'antenatal: {self.subject_identifier}'

    @property
    def caregiver_offstudy_dt(self):
        caregiver_offstudy_cls = django_apps.get_model(
            'flourish_prn.caregiveroffstudy')
        try:
            offstudy = caregiver_offstudy_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except caregiver_offstudy_cls.DoesNotExist:
            return None
        else:
            offstudy_dt = getattr(offstudy, 'offstudy_date', None)
            return offstudy_dt

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
