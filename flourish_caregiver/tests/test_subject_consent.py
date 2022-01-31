import re

from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, YES
from edc_facility.import_holidays import import_holidays
from edc_registration.models import RegisteredSubject
from model_mommy import mommy

from ..models import SubjectConsent, ScreeningPregWomen, ScreeningPriorBhpParticipants

subject_identifier = '[B|C]142\-[0-9\-]+'


class TestSubjectConsent(TestCase):

    def setUp(self):
        import_holidays()
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
            'consent_copy': YES}

    def test_allocated_subject_identifier_invalid(self):
        """Test consent does not allocate subject identifier on
        save if participant is ineligible.
        """
        options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow,
            'breastfeed_intent': NO}
        mommy.make_recipe('flourish_caregiver.subjectconsent', **options)
        self.assertIsNone(SubjectConsent.objects.all()[0].subject_identifier)

    def test_allocated_subject_identifier(self):
        """Test consent allocates subject identifier on save if participant
        is eligible.
        """
        consent = mommy.make_recipe('flourish_caregiver.subjectconsent',
                                    **self.eligible_options)
        self.assertTrue(
            re.match(
                subject_identifier,
                SubjectConsent.objects.all()[0].subject_identifier))

    def test_consent_creates_registered_subject_invalid(self):
        """Test consent does not create a registered subject on
        save if participant is ineligible.
        """
        options = {
            'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow,
            'breastfeed_intent': NO}
        self.assertEquals(RegisteredSubject.objects.all().count(), 0)
        mommy.make_recipe('flourish_caregiver.subjectconsent', **options)
        self.assertEquals(RegisteredSubject.objects.all().count(), 0)

    def test_consent_creates_registered_subject(self):
        """Test consent creates a registered subject on save if participant is eligible.
        """
        self.assertEquals(RegisteredSubject.objects.all().count(), 0)
        mommy.make_recipe('flourish_caregiver.subjectconsent', **self.eligible_options)
        self.assertEquals(RegisteredSubject.objects.all().count(), 1)

    @tag('identifiers')
    def test_screening_updates_subject_identifier(self):
        """Test if subject identifiers for the screening model is being updated after
        saving the consent
        """
        consent_obj = mommy.make_recipe('flourish_caregiver.subjectconsent',
                                        **self.eligible_options)
        screening_obj = ScreeningPriorBhpParticipants.objects.get(
            screening_identifier=consent_obj.screening_identifier)
        self.assertEquals(screening_obj.subject_identifier,
                          consent_obj.subject_identifier)
