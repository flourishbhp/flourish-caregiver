from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from model_mommy import mommy

from flourish_caregiver.subject_helper_mixin import SubjectHelperMixin


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
            protocol=None, age_year=None, age_month=None, efv=None,
            subject_identifier=None):
        """Creates a 5.1-year-old by year 3 participant's mother who is on
        efv regimen from Mpepu study is put on cohort b schedule.

        Returns:
        - The subject identifier of the participant's child.
        """
        self.subject_identifier = subject_identifier
        self.study_maternal_identifier = '981232'
        self.maternal_dataset_options['protocol'] = protocol
        self.maternal_dataset_options['delivdt'] = self.year_3_age(age_year, age_month)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            preg_efv=efv,
            **self.maternal_dataset_options)

        mommy.make_recipe(
            'flourish_child.childdataset',
            dob=self.year_3_age(age_year, age_month),
            **self.child_dataset_options)

        sh = SubjectHelperMixin()

        _subject_identifier = sh.enroll_prior_participant(
            maternal_dataset_obj.screening_identifier,
            study_child_identifier=self.child_dataset_options['study_child_identifier'])

        return _subject_identifier

    def get_cohort_a_subj(self):
        return self.enrollment_and_cohort_assignment(
            protocol='Tshilo Dikotla',
            age_year=4,
            age_month=1,
            subject_identifier='12345678'
        )

    def get_cohort_b_subj(self):
        return self.enrollment_and_cohort_assignment(
            protocol='Mpepu',
            age_year=6,
            age_month=1,
            efv=1,
            subject_identifier='12345678'
        )

    def get_cohort_c_subj(self):
        return self.enrollment_and_cohort_assignment(
            protocol='Tshipidi', age_year=11,
            age_month=1,
            subject_identifier='12345678')
