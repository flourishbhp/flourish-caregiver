from dateutil.relativedelta import relativedelta
from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_constants.constants import IND, NEG, POS, UNK, YES

from .enrollment_helper import EnrollmentHelper
from .utils import get_locator_model_obj


class MaternalStatusHelper(object):

    def __init__(self, maternal_visit=None, subject_identifier=None,
                 study_maternal_identifier=None):
        self.maternal_visit = maternal_visit
        self.subject_identifier = (subject_identifier or
                                   getattr(self.maternal_visit, 'subject_identifier', None))

        self.study_maternal_identifier = study_maternal_identifier

    @property
    def hiv_status(self):
        """Return an HIV status.
        """
        rapid_test_result_cls = django_apps.get_model(
            'flourish_caregiver.hivrapidtestcounseling')
        try:
            rapid_test_result = rapid_test_result_cls.objects.filter(
                maternal_visit__subject_identifier=self.subject_identifier,
                rapid_test_done=YES).latest(
                    'report_datetime')
        except rapid_test_result_cls.DoesNotExist:
            pass
        else:
            status = self._evaluate_status_from_rapid_tests(
                (rapid_test_result, 'result', 'result_date'))
            if status in [POS, NEG, UNK, IND]:
                return status

        # If we have exhausted all visits without a concrete status then use
        # enrollment.
        antenatal_enrollment_cls = django_apps.get_model(
            'flourish_caregiver.antenatalenrollment')
        antenatal_enrollments = antenatal_enrollment_cls.objects.filter(
            subject_identifier=self.subject_identifier,)
        for antenatal_enrollment in antenatal_enrollments:
            status = self._evaluate_status_from_rapid_tests(
                (antenatal_enrollment, 'enrollment_hiv_status', 'rapid_test_date'))
            if status == UNK:
                # Check that the week32_test_date is still within 3 months
                status = self._evaluate_status_from_rapid_tests(
                    (antenatal_enrollment, 'enrollment_hiv_status',
                        'week32_test_date'))
            if status in [POS, NEG, UNK]:
                return status
        return self.enrollment_hiv_status

    @property
    def subject_consent(self):
        subject_consent_cls = django_apps.get_model(
            'flourish_caregiver.subjectconsent')
        try:
            subject_consent = subject_consent_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except subject_consent_cls.DoesNotExist:
            return None
        else:
            return subject_consent

    @property
    def enrollment_hiv_status(self):
        """Returns caregiver's current hiv status.
        """

        maternal_dataset_cls = django_apps.get_model(
            'flourish_caregiver.maternaldataset')

        previous_enrollment_cls = django_apps.get_model(
            'flourish_caregiver.caregiverpreviouslyenrolled')

        antenatal_enrollment_cls = django_apps.get_model(
            'flourish_caregiver.antenatalenrollment')

        try:
            previous_enrollment = previous_enrollment_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except previous_enrollment_cls.DoesNotExist:
            try:
                antenatal_enrollment = antenatal_enrollment_cls.objects.get(
                    subject_identifier=self.subject_identifier)
            except antenatal_enrollment_cls.DoesNotExist:
                # To refactor to include new enrollees
                pass
            else:
                enrollment_helper = EnrollmentHelper(
                    instance_antenatal=antenatal_enrollment,
                    exception_cls=forms.ValidationError)
                try:
                    return enrollment_helper.enrollment_hiv_status
                except ValidationError:
                    return UNK
        else:
            if previous_enrollment.current_hiv_status is not None:
                return previous_enrollment.current_hiv_status

        maternal_dataset_objs = None
        locator_obj = None

        if self.subject_identifier:
            locator_obj = get_locator_model_obj(self.subject_identifier)

        study_maternal_identifier = getattr(
            locator_obj, 'study_maternal_identifier', None) or self.study_maternal_identifier

        if study_maternal_identifier:
            maternal_dataset_objs = maternal_dataset_cls.objects.filter(
                study_maternal_identifier=study_maternal_identifier)

        # for maternal_dataset_obj in maternal_dataset_objs:
        if maternal_dataset_objs:
            mom_hiv_statuses = maternal_dataset_objs.values_list(
                'mom_hivstatus', flat=True)

            if 'HIV-infected' in mom_hiv_statuses:
                return POS
            else:
                return NEG

        return UNK

    @property
    def eligible_for_cd4(self):
        """Return True is one is eligible for cd4.
        """
        maternal_interim_idcc_cls = django_apps.get_model(
            'flourish_caregiver.maternalinterimidcc')
        latest_interim_idcc = None
        latest_visit = self.previous_visits.first()
        try:
            latest_interim_idcc = maternal_interim_idcc_cls.objects.get(
                maternal_visit=latest_visit)
        except maternal_interim_idcc_cls.DoesNotExist:
            pass
        else:
            three_month_back = latest_visit.report_datetime.date() - relativedelta(
                months=3)
            if latest_interim_idcc.recent_cd4_date:
                if (three_month_back > latest_interim_idcc.recent_cd4_date
                        and self.hiv_status == POS):
                    return True
                else:
                    return False
        return True

    @property
    def previous_visits(self):
        return self.maternal_visit.__class__.objects.filter(
            subject_identifier=self.maternal_visit.subject_identifier).order_by(
            '-appointment__timepoint')

    def _evaluate_status_from_rapid_tests(self, instance_result_date_tuple):
        """Return an HIV status.
        """

        if getattr(instance_result_date_tuple[0], instance_result_date_tuple[1]) == POS:
            return POS
        if getattr(instance_result_date_tuple[0], instance_result_date_tuple[1]) == IND:
            return IND
        elif (getattr(instance_result_date_tuple[0], instance_result_date_tuple[1]) == NEG
              and getattr(instance_result_date_tuple[0], instance_result_date_tuple[2])):
            if (self.maternal_visit
                    and getattr(instance_result_date_tuple[0],
                                instance_result_date_tuple[2])
                    > (self.maternal_visit.report_datetime.date() - relativedelta(
                        months=3))):
                return NEG
            return NEG
        else:
            if getattr(instance_result_date_tuple[0], instance_result_date_tuple[1]) == UNK:
                return UNK
