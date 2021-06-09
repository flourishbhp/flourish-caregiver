import re
from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy

from ..models import SubjectConsent
from edc_constants.constants import NO, YES

subject_identifier = '[B|C]142\-[0-9\-]+'


class TestSubjectIdentifier(TestCase):

    def setUp(self):
        import_holidays()

        self.subject_screening = mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants')

        self.eligible_options = {
            # 'screening_identifier': self.subject_screening.screening_identifier,
            'consent_datetime': get_utcnow,
            'remain_in_study': YES,
            'hiv_testing': YES,
            'breastfeed_intent': YES,
            'consent_reviewed': YES,
            'study_questions': YES,
            'assessment_score': YES,
            'consent_signature': YES,
            'consent_copy': YES}

    def test_subject_identifier_bio_mother(self):
        """Test consent allocates subject identifier starting with a B for a
        biological mother.
        """
        self.eligible_options.update(biological_caregiver=YES)
        mommy.make_recipe('flourish_caregiver.subjectconsent', **self.eligible_options)
        self.assertTrue(
            re.match(
                subject_identifier,
                SubjectConsent.objects.all()[0].subject_identifier))

    def test_subject_identifier_bio_mother2(self):
        """Test consent allocates subject identifier starting with a B for a
        biological mother.
        """
        subject_screening = mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants', mother_alive=YES)
        self.eligible_options.update(
            screening_identifier=subject_screening.screening_identifier,
            biological_caregiver=YES)

        mommy.make_recipe('flourish_caregiver.subjectconsent', **self.eligible_options)
        subject_identifier = SubjectConsent.objects.all()[0].subject_identifier
        self.assertTrue(subject_identifier.startswith('B'))

    def test_subject_identifier_caregiver(self):
        """Test consent allocates subject identifier starting with a C for a
        non biological mother.
        """
        self.eligible_options.update(biological_caregiver=NO)
        mommy.make_recipe('flourish_caregiver.subjectconsent', **self.eligible_options)
        self.assertTrue(
            re.match(
                subject_identifier,
                SubjectConsent.objects.all()[0].subject_identifier))

    def test_subject_identifier_caregiver2(self):
        """Test consent allocates subject identifier starting with a C for a
         non biological mother.
        """
        self.eligible_options.update(biological_caregiver=NO)
        mommy.make_recipe('flourish_caregiver.subjectconsent', **self.eligible_options)
        subject_identifier = SubjectConsent.objects.all()[0].subject_identifier
        self.assertTrue(subject_identifier.startswith('C'))

    @tag('si')
    def test_check_digit_sequential(self):
        """Test child subject identifier's postfix increments correctly.
        """
        subject_consent = mommy.make_recipe('flourish_caregiver.subjectconsent',
                                            **self.eligible_options)

        child_consent1 = mommy.make_recipe('flourish_caregiver.caregiverchildconsent',
                                           subject_consent=subject_consent,
                                           identity=None,
                                           confirm_identity=None,
                                           identity_type=None)

        child_consent2 = mommy.make_recipe('flourish_caregiver.caregiverchildconsent',
                                           subject_consent=subject_consent,
                                           child_dob=(get_utcnow() - relativedelta(years=13)).date(),
                                           identity=None,
                                           confirm_identity=None,
                                           identity_type=None)

        child_consent3 = mommy.make_recipe('flourish_caregiver.caregiverchildconsent',
                                           subject_consent=subject_consent,
                                           child_dob=(get_utcnow() - relativedelta(years=14)).date(),
                                           identity=None,
                                           confirm_identity=None,
                                           identity_type=None)

        child_consent4 = mommy.make_recipe('flourish_caregiver.caregiverchildconsent',
                                           subject_consent=subject_consent,
                                           child_dob=(get_utcnow() - relativedelta(years=10)).date(),
                                           identity=None,
                                           confirm_identity=None,
                                           identity_type=None)

        self.assertTrue(
            re.match(
                child_consent1.subject_identifier, subject_consent.subject_identifier + '-10'))

        self.assertTrue(
            re.match(
                child_consent2.subject_identifier, subject_consent.subject_identifier + '-60'))

        self.assertTrue(
            re.match(
                child_consent3.subject_identifier, subject_consent.subject_identifier + '-70'))

        self.assertTrue(
            re.match(
                child_consent4.subject_identifier, subject_consent.subject_identifier + '-80'))

