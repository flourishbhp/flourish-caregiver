from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base import get_utcnow
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from ..models.onschedule import OnScheduleCohortATb2Months


@tag('tb')
class TestVisitScheduleTb(TestCase):

    def setUp(self):
        import_holidays()
        self.subject_identifier = '12345678'
        self.study_maternal_identifier = '89721'

        self.options = {
            'consent_datetime': get_utcnow(),
            'version': '1'
            }

        self.subject_screening = mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants')

        self.eligible_options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow,
            'remain_in_study': YES,
            'hiv_testing': YES,
            'breastfeed_intent': YES,
            'consent_reviewed': YES,
            'study_questions': YES,
            'assessment_score': YES,
            'consent_signature': YES,
            'consent_copy': YES
            }

    def test_put_on_tb_schedule(self):
        consent = mommy.make_recipe('flourish_caregiver.subjectconsent',
                                    **self.eligible_options)
        mommy.make_recipe(
            'flourish_caregiver.tbinformedconsent',
            subject_identifier=consent.subject_identifier,
            )

        self.assertEqual(OnScheduleCohortATb2Months.objects.filter(
            subject_identifier=consent.subject_identifier,
            schedule_name='tb_2_months_schedule').count(), 1)
