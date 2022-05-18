from django.core.exceptions import ValidationError
from django.db import models
from edc_action_item.model_mixins import ActionModelMixin

from ..action_items import ULTRASOUND_ACTION
from ..choices import GESTATIONS_NUMBER, ZERO_ONE
from ..validators import validate_ga_by_ultrasound, validate_fetal_weight
from .model_mixins import UltraSoundModelMixin, CrfModelMixin


class UltraSound(UltraSoundModelMixin, ActionModelMixin, CrfModelMixin):

    """ The initial ultra sound model that influences mother's
    enrollment in to study.
    """

    tracking_identifier_prefix = 'CU'

    action_name = ULTRASOUND_ACTION

    number_of_gestations = models.CharField(
        verbose_name="Number of viable gestations seen?",
        max_length=3,
        choices=GESTATIONS_NUMBER,
        help_text='If number is not equal to 1, then participant '
        'goes off study.')

    ga_by_lmp = models.IntegerField(
        verbose_name="GA by LMP at ultrasound date",
        null=True,
        blank=True,
        help_text='Units in weeks. Derived variable, see AntenatalEnrollment.')

    ga_by_ultrasound_wks = models.IntegerField(
        verbose_name="GA by ultrasound in weeks",
        validators=[validate_ga_by_ultrasound, ],
        help_text='Units in weeks.')

    ga_by_ultrasound_days = models.IntegerField(
        verbose_name="GA by ultrasound days offset",
        help_text='must be less than 7days.')

    est_fetal_weight = models.DecimalField(
        verbose_name="Estimated fetal weight",
        validators=[validate_fetal_weight, ],
        max_digits=8,
        decimal_places=2,
        help_text='Units in grams.')

    est_edd_ultrasound = models.DateField(
        verbose_name="Estimated date of delivery by ultrasound",
        help_text='EDD')

    edd_confirmed = models.DateField(
        verbose_name="EDD Confirmed.",
        help_text='EDD Confirmed. Derived variable, see AntenatalEnrollment.')

    ga_confirmed = models.IntegerField(
        verbose_name="GA by Scan.",
        help_text='Derived variable.')

    ga_confrimation_method = models.CharField(
        verbose_name="The method used to derive edd_confirmed.",
        max_length=3,
        choices=ZERO_ONE,
        help_text='0=EDD Confirmed by edd_by_lmp, 1=EDD Confirmed by'
        ' edd_by_ultrasound.')

    def save(self, *args, **kwargs):
        # What if values in AntenatalEnrollment change?
        # They cannot. Antenatal Enrollment cannot be updated once UltraSound
        #         form has gone in without DMC intervention.
        # This is because it can potentially affect enrollment eligibility.
        self.ga_by_lmp = self.evaluate_ga_by_lmp()
        self.edd_confirmed, ga_c_m = self.evaluate_edd_confirmed()
        self.ga_confrimation_method = ga_c_m
        self.ga_confirmed = self.evaluate_ga_confirmed()
        self.subject_identifier = self.maternal_visit.appointment.subject_identifier
        super(UltraSound, self).save(*args, **kwargs)

    @property
    def pass_antenatal_enrollment(self):
        return int(self.number_of_gestations) == 1

    def evaluate_ga_by_lmp(self):
        return (int(abs(40 - ((self.antenatal_enrollment.edd_by_lmp -
                               self.report_datetime.date()).days / 7))) if
                self.antenatal_enrollment.edd_by_lmp else None)

    def evaluate_edd_confirmed(self, error_clss=None):
        ga_by_lmp = self.evaluate_ga_by_lmp()
        edd_by_lmp = self.antenatal_enrollment.edd_by_lmp
        if not edd_by_lmp:
            return (self.est_edd_ultrasound, 1)
        error_clss = error_clss or ValidationError
        if ga_by_lmp > 16 and ga_by_lmp < 22:
            if abs((edd_by_lmp - self.est_edd_ultrasound).days) > 10:
                return (self.est_edd_ultrasound, 1)
            else:
                return (edd_by_lmp, 0)
        elif ga_by_lmp > 22 and ga_by_lmp < 28:
            if abs((edd_by_lmp - self.est_edd_ultrasound).days) > 14:
                return (self.est_edd_ultrasound, 1)
            else:
                return (edd_by_lmp, 0)
        elif ga_by_lmp > 28:
            if abs((edd_by_lmp - self.est_edd_ultrasound).days) > 21:
                return (self.est_edd_ultrasound, 1)
            else:
                return (edd_by_lmp, 0)
        else:
            return (edd_by_lmp, 0)

    def evaluate_ga_confirmed(self):
        return int(
            abs(40 - (
                (self.edd_confirmed - self.report_datetime.date()).days / 7)))

    @property
    def action_item_reason(self):
        return 'Number of gestations is ' + self.number_of_gestations

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'UltraSound Form'
        verbose_name_plural = 'UltraSound Form'
