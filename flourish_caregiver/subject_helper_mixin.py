from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from .models import CaregiverLocator, MaternalDataset


class SubjectHelperMixin:

    def create_cohort_c_dataset(self):

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=10, months=2),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '8907-21',
            'preg_pi': 1,
            'protocol': 'Tshipidi'}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Unexposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '8907-21',
            'study_child_identifier': '1234'}

        mommy.make_recipe(
            'flourish_child.childdataset',
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            **self.maternal_dataset_options)

        return maternal_dataset_obj

    def create_antenatal_enrollment(self, **kwargs):
        import_holidays()

        preg_screening = mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',)

        self.options = {
            'consent_datetime': get_utcnow(),
            'screening_identifier': preg_screening.screening_identifier,
            'breastfeed_intent': YES,
            'version': '1'}

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            **self.options)

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier,)

        mommy.make_recipe(
            'flourish_caregiver.caregiverlocator',
            subject_identifier=subject_consent.subject_identifier,)

        return subject_consent.subject_identifier

    def create_TD_efv_enrollment(self, screening_identifier, **kwargs):
        import_holidays()

        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            prior_screening = mommy.make_recipe(
                'flourish_caregiver.screeningpriorbhpparticipants',
                screening_identifier=maternal_dataset_obj.screening_identifier)

            consent_options = {
                'consent_datetime': get_utcnow(),
                'screening_identifier': prior_screening.screening_identifier,
                'breastfeed_intent': YES,
                'version': '1'}

            subject_consent = mommy.make_recipe(
                'flourish_caregiver.subjectconsent',
                ** consent_options)

            mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                child_dob=maternal_dataset_obj.delivdt,)

            mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled')

            return subject_consent.subject_identifier
        return None

    def create_TD_no_hiv_enrollment(self, screening_identifier, **kwargs):
        import_holidays()

        self.maternal_dataset_options['mom_hivstatus'] = 'HIV uninfected'

        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            prior_screening = mommy.make_recipe(
                'flourish_caregiver.screeningpriorbhpparticipants',
                screening_identifier=maternal_dataset_obj.screening_identifier)

            consent_options = {
                'consent_datetime': get_utcnow(),
                'screening_identifier': prior_screening.screening_identifier,
                'breastfeed_intent': YES,
                'version': '1'}

            subject_consent = mommy.make_recipe(
                'flourish_caregiver.subjectconsent',
                ** consent_options)

            mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                child_dob=maternal_dataset_obj.delivdt,)

            mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled')

            return subject_consent.subject_identifier
        return None

    def prepare_prior_participant_enrollment(self, maternal_dataset_obj):

        try:
            caregiver_locator = CaregiverLocator.objects.get(
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,)
        except CaregiverLocator.DoesNotExist:
            caregiver_locator = mommy.make_recipe(
                'flourish_caregiver.caregiverlocator',
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,
                screening_identifier=maternal_dataset_obj.screening_identifier)

        worklist_cls = django_apps.get_model('flourish_follow.worklist')
        try:
            worklist_cls.objects.get(
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)
        except worklist_cls.DoesNotExist:
            mommy.make_recipe(
                'flourish_follow.worklist',
                subject_identifier=None,
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,
                user_created='flourish')

        call = mommy.make_recipe(
            'flourish_follow.call',
            label='worklistfollowupmodelcaller')

        log = mommy.make_recipe(
            'flourish_follow.log',
            call=call,)

        mommy.make_recipe(
            'flourish_follow.logentry',
            log=log,
            study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,
            user_created='flourish')
        return caregiver_locator

    def enroll_prior_participant(self, screening_identifier, study_child_identifier):

        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            self.options = {
                'consent_datetime': get_utcnow(),
                'version': '1'}

            mommy.make_recipe(
                'flourish_caregiver.screeningpriorbhpparticipants',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)

            subject_consent = mommy.make_recipe(
                'flourish_caregiver.subjectconsent',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                breastfeed_intent=NOT_APPLICABLE,
                biological_caregiver=YES,
                **self.options)

            mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                study_child_identifier=study_child_identifier,
                child_dob=maternal_dataset_obj.delivdt,)

            mommy.make_recipe(
                    'flourish_caregiver.caregiverpreviouslyenrolled',
                    subject_identifier=subject_consent.subject_identifier)
            return subject_consent.subject_identifier

    def enroll_prior_participant_assent(self, screening_identifier, study_child_identifier,
                                        consent_datetime=None):

        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            self.options = {
                'consent_datetime': consent_datetime or get_utcnow(),
                'version': '1'}

            mommy.make_recipe(
                'flourish_caregiver.screeningpriorbhpparticipants',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)

            subject_consent = mommy.make_recipe(
                'flourish_caregiver.subjectconsent',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                breastfeed_intent=NOT_APPLICABLE,
                **self.options)

            caregiver_child_consent_obj = mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                study_child_identifier=study_child_identifier,
                child_dob=maternal_dataset_obj.delivdt,)

            mommy.make_recipe(
                'flourish_child.childassent',
                subject_identifier=caregiver_child_consent_obj.subject_identifier,
                first_name=caregiver_child_consent_obj.first_name,
                last_name=caregiver_child_consent_obj.last_name,
                dob=caregiver_child_consent_obj.child_dob,
                identity=caregiver_child_consent_obj.identity,
                confirm_identity=caregiver_child_consent_obj.identity,
                remain_in_study=YES,
                version=subject_consent.version)

            mommy.make_recipe(
                    'flourish_caregiver.caregiverpreviouslyenrolled',
                    subject_identifier=subject_consent.subject_identifier)

            return subject_consent.subject_identifier
