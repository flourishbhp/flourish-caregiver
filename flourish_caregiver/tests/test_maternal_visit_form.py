from django.core.exceptions import ValidationError
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import OFF_STUDY, ON_STUDY, NOT_APPLICABLE
from edc_constants.constants import UNKNOWN, DEAD, ALIVE, YES, PARTICIPANT, NO
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import LOST_VISIT
from edc_appointment.models import Appointment
from model_mommy import mommy

from ..forms import MaternalVisitFormValidator

@tag('visitvalid')
class TestMaternalVisitFormValidator(TestCase):

    def setUp(self):
        import_holidays()

        self.options = {
            'consent_datetime': get_utcnow(),
            'breastfeed_intent': NOT_APPLICABLE,
            'version': '1'}

        self.screening_preg = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen')

        self.subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            screening_identifier=self.screening_preg.screening_identifier,
            **self.options)

        child = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=self.subject_consent,
            child_dob=None,
            first_name=None,
            last_name=None, )

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            child_subject_identifier=child.subject_identifier,
            subject_identifier=self.subject_consent.subject_identifier,)

        self.appointment = Appointment.objects.get(visit_code='1000M')

    def test_study_status_on_dead_valid(self):

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }

        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_last_alive_date_not_required_valid(self):
        cleaned_data = {
            'pk': 'hhdks',
            'report_datetime': get_utcnow(),
            'survival_status': UNKNOWN,
            'last_alive_date': None,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_death_study_status_invalid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': DEAD,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('study_status', form_validator._errors)

    def test_death_study_status_valid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': DEAD,
            'last_alive_date': get_utcnow().date(),
            'study_status': OFF_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_unknown_study_status_invalid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': UNKNOWN,
            'last_alive_date': get_utcnow().date(),
            'study_status': OFF_STUDY,
            'info_source': PARTICIPANT,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('survival_status', form_validator._errors)

        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': UNKNOWN,
            'last_alive_date': get_utcnow().date(),
            'study_status': OFF_STUDY,
            'info_source': 'blahblah',
            'is_present': YES,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('survival_status', form_validator._errors)

    def test_unknown_study_status_valid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': DEAD,
            'last_alive_date': get_utcnow().date(),
            'study_status': OFF_STUDY,
            'info_source': 'blahblah',
            'is_present': NO,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_reason_offstudy_invalid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'reason': LOST_VISIT,
            'is_present': NO,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('study_status', form_validator._errors)

    def test_reason_offstudy_valid(self):
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'reason': LOST_VISIT,
            'last_alive_date': get_utcnow().date(),
            'study_status': OFF_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')

    def test_is_presnt_info_source_invalid(self):
        self.subject_consent = None
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'is_present': YES,
            'info_source': 'blahblah',
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        self.assertRaises(ValidationError, form_validator.validate)
        self.assertIn('info_source', form_validator._errors)

    def test_is_presnt_info_source_valid(self):
        self.subject_consent = None
        cleaned_data = {
            'report_datetime': get_utcnow(),
            'survival_status': ALIVE,
            'is_present': YES,
            'info_source': PARTICIPANT,
            'last_alive_date': get_utcnow().date(),
            'study_status': ON_STUDY,
            'appointment': self.appointment
        }
        form_validator = MaternalVisitFormValidator(
            cleaned_data=cleaned_data)
        try:
            form_validator.validate()
        except ValidationError as e:
            self.fail(f'ValidationError unexpectedly raised. Got{e}')
