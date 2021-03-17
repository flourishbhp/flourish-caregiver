from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_facility.import_holidays import import_holidays
from ..subject_helper_mixin import SubjectHelperMixin
from ..models import MaternalDataset, ScreeningPriorBhpParticipants, SubjectConsent


@tag('sh')
class TestSubjectHelperMixin(TestCase):

    def setUp(self):
        import_holidays()
        self.subject_helper = SubjectHelperMixin()

    def test_prior_participant_creation(self):

        self.subject_helper.create_TD_efv_enrollment(subject_identifier='142-40200037')

        self.assertEqual(ScreeningPriorBhpParticipants.objects.all().count(), 1)

        self.assertEqual(MaternalDataset.objects.all().count(), 1)

        self.assertEqual(SubjectConsent.objects.all().count(), 1)

    def prepare_prior_participant_enrolmment(self):

        subject_identifier = self.subject_helper.create_TD_efv_enrollment(
            subject_identifier='142-40200037')

        maternal_dataset_obj = MaternalDataset.objects.get(
            subject_identifier=subject_identifier)

        self.subject_helper.prepare_prior_participant_enrolmment(maternal_dataset_obj)

        logentry_cls = django_apps.get_model('flourish_follow.logentry')

        self.assertEqual(logentry_cls.objects.all().count(), 1)
