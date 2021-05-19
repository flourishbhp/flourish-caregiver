from django.test import TestCase
from edc_action_item.models.action_item import ActionItem
from edc_base.utils import get_utcnow
from edc_constants.constants import CLOSED
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from edc_appointment.models import Appointment
from dateutil.relativedelta import relativedelta
from edc_appointment.constants import INCOMPLETE_APPT

from ..models import CaregiverLocator
from ..subject_helper_mixin import SubjectHelperMixin


class TestCaregiverLocatorAction(TestCase):

    def setUp(self):
        import_holidays()

        self.subject_identifier = '12345678'

        self.subject_identifier = self.subject_identifier[:-1] + '2'
        self.study_maternal_identifier = '981232'

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'}

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=2, months=5),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': self.study_maternal_identifier,
            'protocol': 'Tshilo Dikotla'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': self.study_maternal_identifier,
            'study_child_identifier': '1234'}

        self.maternal_dataset_options['protocol'] = 'Mpepu'
        self.maternal_dataset_options[
            'delivdt'] = get_utcnow() - relativedelta(years=5,
                                                      months=2)
        self.maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=1,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.caregiverlocator',
            screening_identifier=self.maternal_dataset_obj.screening_identifier)

        self.sh = SubjectHelperMixin()

    def test_caregiver_locator_subject_identifier_updated(self):

        subject_identifier = self.sh.enroll_prior_participant(
            self.maternal_dataset_obj.screening_identifier)

        caregiver_locator_obj = CaregiverLocator.objects.get(
            screening_identifier=self.maternal_dataset_obj.screening_identifier)

        self.assertEqual(
            caregiver_locator_obj.subject_identifier, subject_identifier)

    def test_action_item_subject_identifier_updated(self):

        subject_identifier = self.sh.enroll_prior_participant(
            self.maternal_dataset_obj.screening_identifier)

        caregiver_locator_obj = CaregiverLocator.objects.get(
            screening_identifier=self.maternal_dataset_obj.screening_identifier)

        action_item_obj = ActionItem.objects.get(
            action_identifier=caregiver_locator_obj.action_identifier)

        self.assertEqual(
            subject_identifier,
            action_item_obj.subject_identifier)

    def test_action_item_closed(self):
        subject_identifier = self.sh.enroll_prior_participant(
            self.maternal_dataset_obj.screening_identifier)

        self.assertEqual(ActionItem.objects.filter(
            status=CLOSED,
            subject_identifier=subject_identifier,
            reference_model='flourish_caregiver.caregiverlocator',).count(), 1)
