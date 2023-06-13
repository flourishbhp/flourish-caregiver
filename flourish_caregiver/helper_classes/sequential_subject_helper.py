from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from model_mommy import mommy

from flourish_caregiver.models import CaregiverChildConsent, \
    CaregiverPreviouslyEnrolled, \
    MaternalDataset, \
    SubjectConsent
from flourish_caregiver.subject_helper_mixin import SubjectHelperMixin
from flourish_child.models import ChildDataset


class SequentialSubjectHelper:
    """A class representing a study participant.

    Attributes:
    - maternal_dataset_options (obj): dict of options to create maternal dataset obj
    - child_dataset_options (obj): dict of options to create child dataset obj
    """

    def __init__(self, maternal_dataset_options, child_dataset_options):
        """
        Initializes a Participant object with the given attributes.
        """
        self.child_dataset_options = child_dataset_options
        self.maternal_dataset_options = maternal_dataset_options

    def year_3_age(self, years, months):
        """Returns the age at year 3.
        """
        app_config = django_apps.get_app_config('flourish_caregiver')
        start_date_year_3 = app_config.start_date_year_3

        child_dob = start_date_year_3 - relativedelta(years=years,
                                                      months=months)
        return child_dob

    def enrollment_and_cohort_assignment(self,
                                         protocol=None, age_year=None, age_month=None,
                                         efv=None,
                                         dob=None, screening_identifier=None,
                                         subject_identifier=None, create_dataset=True):
        """Creates a 5.1-year-old by year 3 participant's mother who is on
        efv regimen from Mpepu study is put on cohort b schedule.

        Returns:
        - The subject identifier of the participant's child.
        """
        if create_dataset:
            maternal_dataset_obj = self.create_dataset(
                subject_identifier=subject_identifier,
                protocol=protocol, dob=dob, efv=efv)

            sh = SubjectHelperMixin()

            _subject_identifier = sh.enroll_prior_participant(
                maternal_dataset_obj.screening_identifier,
                study_child_identifier=self.child_dataset_options[
                    'study_child_identifier'])

        else:
            _subject_identifier = self.update_dataset(
                subject_identifier=subject_identifier, dob=dob)

        return _subject_identifier

    def update_dataset(self, subject_identifier, dob):
        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                subject_identifier=subject_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            try:
                child_dataset_obj = ChildDataset.objects.get(
                    study_maternal_identifier=maternal_dataset_obj
                    .study_maternal_identifier)
            except ChildDataset.DoesNotExist:
                pass
            else:
                child_dataset_obj.dob = dob
                child_dataset_obj.save()
            maternal_dataset_obj.delivdt = dob
            maternal_dataset_obj.save()
            subject_consent = self.update_consent(
                subject_identifier=subject_identifier)
            self.update_caregiver_child_consent(subject_consent=subject_consent, dob=dob)
            self.resave_caregiver_previously_enrolled(
                subject_identifier=subject_identifier)
            return subject_identifier

    def resave_caregiver_previously_enrolled(self, subject_identifier):
        try:
            caregiver_previously_enrolled_obj = CaregiverPreviouslyEnrolled.objects.get(
                subject_identifier=subject_identifier
            )
        except CaregiverPreviouslyEnrolled.DoesNotExist:
            pass
        else:
            caregiver_previously_enrolled_obj.save()

    def update_caregiver_child_consent(self, subject_consent, dob):
        try:
            caregiver_child_consent_obj = CaregiverChildConsent.objects.get(
                subject_consent=subject_consent
            )
        except CaregiverChildConsent.DoesNotExist:
            pass
        else:
            caregiver_child_consent_obj.child_dob = dob
            caregiver_child_consent_obj.save()
            return caregiver_child_consent_obj

    def update_consent(self, subject_identifier):
        try:
            subject_consent = SubjectConsent.objects.get(
                subject_identifier=subject_identifier
            )
        except SubjectConsent.DoesNotExist:
            pass
        else:
            return subject_consent

    def create_dataset(self, subject_identifier, protocol, dob, efv):
        self.subject_identifier = subject_identifier
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = protocol
        self.maternal_dataset_options['delivdt'] = dob

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=efv,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=dob,
            **self.child_dataset_options)

        return maternal_dataset_obj

    def get_cohort_a_subj(self):
        dob = self.year_3_age(4, 1)
        return self.enrollment_and_cohort_assignment(
            protocol='Tshilo Dikotla',
            age_year=4,
            age_month=1,
            subject_identifier='12345678',
            dob=dob
        )

    def get_cohort_b_subj(self):
        dob = self.year_3_age(6, 1)
        return self.enrollment_and_cohort_assignment(
            protocol='Mpepu',
            age_year=6,
            age_month=1,
            efv=1,
            dob=dob,
            subject_identifier='12345678'
        )

    def get_cohort_c_subj(self):
        dob = self.year_3_age(11, 1)
        return self.enrollment_and_cohort_assignment(
            protocol='Tshipidi', age_year=11,
            age_month=1,
            dob=dob,
            subject_identifier='12345678')
