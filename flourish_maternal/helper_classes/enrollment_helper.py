from dateutil.relativedelta import relativedelta
from django import forms
from edc_constants.constants import NO, YES, POS, NEG


class EnrollmentError(Exception):
    pass


class EnrollmentHelper(object):

    """Class that determines maternal eligibility based on the protocol
    specific criteria.

    * Accepts an instance_antenatal of AntenatalEnrollment or
    PostnatalEnrollment.
    * is called in the save method of the EnrollmentMixin.
    * makes available the calculated enrollment_hiv_status and date_at_32wks
      which can be saved to the model instance_antenatal.

    Note: it's assumed the form validates values to avoid raising an
    EnrollmentError here.

    For example:

    def save(self, *args, **kwargs):
        enrollment_helper = EnrollmentHelper(instance_antenatal=self)
        self.is_eligible = enrollment_helper.is_eligible
        self.enrollment_hiv_status = enrollment_helper.enrollment_hiv_status
        self.date_at_32wks = enrollment_helper.date_at_32wks
        super(EnrollmentMixin, self).save(*args, **kwargs)
    """

    def __init__(self, instance_antenatal, exception_cls=None):
        self.instance_antenatal = instance_antenatal
        self.date_at_32wks = (
            self.evaluate_edd_by_lmp - relativedelta(weeks=6) if
            self.evaluate_edd_by_lmp else None)
        self.exception_cls = exception_cls or EnrollmentError

    @property
    def enrollment_hiv_status(self):
        """Returns the maternal HIV status at enrollment based on valid
        combinations
        expected from the form otherwise raises a EnrollmentError.
        Can only return POS or NEG.

        Note: the EnrollmentError should never be excepted!!
        """

        pos = self.known_hiv_pos_with_evidence(
        ) or self.tested_pos_at32wks()

        neg = (self.tested_neg_at32wks() or
               self.tested_neg_previously_result_within_3_months())

        if self.rapidtest_result() in [POS, NEG]:
            return self.rapidtest_result()
        elif neg and not pos:
            return NEG
        elif pos and not neg:
            return POS
        else:
            # Case neg and pos OR not neg and not pos
            raise forms.ValidationError(
                'Unable to determine maternal hiv status at enrollment. '
                f'Got current_hiv_status={self.instance_antenatal.current_hiv_status},'
                f'evidence_hiv_status={self.instance_antenatal.evidence_hiv_status},'
                f'rapid_test_done={self.instance_antenatal.rapid_test_done}')

    def known_hiv_pos_with_evidence(self):
        """"""
        if (self.instance_antenatal.current_hiv_status == POS and
                self.instance_antenatal.evidence_hiv_status == YES):
            return True
        return False

    def tested_pos_at32wks(self):
        if (self.instance_antenatal.week32_test == YES and
            self.instance_antenatal.week32_result == POS and
                self.instance_antenatal.evidence_32wk_hiv_status == YES):
            return True
        return False

    def rapidtest_result(self):
        if self.instance_antenatal.rapid_test_done == YES:
            return self.instance_antenatal.rapid_test_result

    def tested_neg_at32wks(self):
        """"""
        if (self.instance_antenatal.week32_test == YES and
            self.test_date_is_on_or_after_32wks() and
                self.instance_antenatal.week32_result == NEG and
                self.instance_antenatal.evidence_32wk_hiv_status == YES):
            return True
        return False

    def tested_neg_previously_result_within_3_months(self):
        """Returns true if the 32 week test date is within 3months else
        false
        """
        if (self.instance_antenatal.week32_test == YES and
            self.instance_antenatal.week32_result == NEG and
            self.instance_antenatal.week32_test_date >
                (self.instance_antenatal.report_datetime.date() -
                 relativedelta(months=3))):
            return True
        return False

    def test_date_is_on_or_after_32wks(self):
        """Returns True if the test date is on or after 32 weeks gestational
        age.
        """
        if self.instance_antenatal.rapid_test_date:
            if (self.instance_antenatal.week32_test_date >
                    self.instance_antenatal.rapid_test_date):
                raise self.exception_cls(
                    'Rapid test date cannot precede test date on or '
                    'after 32 weeks')
        return (
            self.instance_antenatal.week32_test_date >=
            self.date_at_32wks if self.date_at_32wks else None)

    @property
    def validate_rapid_test(self):
        """Returns True to indicate that a rapid test is not required,
        False to indicate a rapid test is required.
        """
        if (self.known_hiv_pos_with_evidence() or
                self.rapidtest_result() in [POS, NEG]):
            return True
        return False

    def raise_validation_error_for_rapidtest(self):
        if (not self.validate_rapid_test and
            self.instance_antenatal.rapid_test_done != YES and
                self.instance_antenatal.rapid_test_result not in [POS, NEG] and
                not self.tested_neg_previously_result_within_3_months()):
            raise self.exception_cls(
                'A rapid test with a valid result of either POS or NEG '
                'is required. Ensure this is the case.')

    @property
    def pending(self):
        """Returns True is Maternal Ultra Sound Initial exists and last mestrual date
        is not known.
        """
        if ((not self.instance_antenatal.ultrasound) and
                (NO in self.instance_antenatal.knows_lmp)):
            return True
        return False

    @property
    def evaluate_edd_by_lmp(self):
        return (
            self.instance_antenatal.last_period_date +
            relativedelta(days=280) if
            self.instance_antenatal.last_period_date else None)

    def evaluate_ga_lmp(self, instance_date):
        return (
            int(40 - ((self.evaluate_edd_by_lmp - instance_date).days / 7)) if
            self.instance_antenatal.last_period_date else None)

    def no_chronic_conditions(self):
        """Returns True if subject has no chronic conditions.
        """
        return (self.instance_antenatal.is_diabetic == NO)
