from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from edc_base.utils import get_utcnow
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy
from .models import CaregiverLocator


class SubjectHelperMixin:

    maternal_dataset_options = {
        'cooking_method': '',
        'delivdt': datetime(2015, 3, 31).date(),
        'delivery_location': 'Molepolole',
        'delivmeth': '',
        'house_type': 'Formal: tin-roofed & concrete walls',
        'live_inhouse_number': 5,
        'mom_age_enrollment': '18-24 years',
        'mom_arvstart_date': datetime(2014, 6, 17).date(),
        'mom_baseline_cd4': 516,
        'mom_education': 'Secondary',
        'mom_enrolldate': datetime(2015, 4, 1).date(),
        'mom_hivstatus': 'HIV-infected',
        'mom_maritalstatus': 'Single',
        'mom_moneysource': 'Relative',
        'mom_occupation': 'Housewife or unemployed',
        'mom_personal_earnings': 'None',
        'mom_pregarv_strat': '3-drug ART',
        'parity': 1,
        'piped_water': 'Other water source',
        'protocol': 'Tshilo Dikotla',
        'site_name': 'Gaborone',
        'study_child_identifier': '142-4995638-1-10',
        'study_maternal_identifier': '142-4995638-1',
        'toilet': 2,
        'toilet_indoors': 'Latrine or none',
        'toilet_private': 'Indoor toilet or private latrine',
        'preg_efv': '1'}

    def create_antenatal_enrollment(self, subject_identifier, **kwargs):
        import_holidays()

        mommy.make_recipe(
            'flourish_caregiver.screeningpregwomen',)

        self.options = {
            'consent_datetime': get_utcnow(),
            'subject_identifier': subject_identifier,
            'screening_identifier': 'A1234',
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

    def create_TD_efv_enrollment(self, subject_identifier, **kwargs):
        import_holidays()

        prior_screening = mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',)

        mommy.make_recipe(
            'flourish_child.childdataset',
            study_child_identifier='142-4995638-1-10',
            infant_hiv_exposed='Exposed',
            subject_identifier=subject_identifier + '-10',)

        mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=subject_identifier,
            screening_identifier=prior_screening.screening_identifier,
            **self.maternal_dataset_options)

        consent_options = {
            'consent_datetime': get_utcnow(),
            'subject_identifier': subject_identifier,
            'screening_identifier': prior_screening.screening_identifier,
            'version': '1'}

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            child_dob=(get_utcnow() - relativedelta(years=2, months=5)).date(),
            ** consent_options)

        return subject_consent.subject_identifier

    def create_TD_no_hiv_enrollment(self, subject_identifier, **kwargs):
        import_holidays()

        self.maternal_dataset_options['mom_hivstatus'] = 'HIV uninfected'

        prior_screening = mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',)

        child_dataset_obj = mommy.make_recipe(
            'flourish_child.childdataset',
            study_child_identifier='142-4975738-1-10',
            infant_hiv_exposed='Exposed',
            subject_identifier=subject_identifier + '-10',)

        mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=subject_identifier,
            study_child_identifier=child_dataset_obj.study_child_identifier,
            study_maternal_identifier='142-4975738-1',
            screening_identifier=prior_screening.screening_identifier,
            **self.maternal_dataset_options)

        consent_options = {
            'consent_datetime': get_utcnow(),
            'subject_identifier': subject_identifier,
            'screening_identifier': prior_screening.screening_identifier,
            'version': '1'}

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            child_dob=(get_utcnow() - relativedelta(years=2, months=8)).date(),
            ** consent_options)

        return subject_consent.subject_identifier

    def prepare_prior_participant_enrolmment(self, maternal_dataset_obj):

        try:
            caregiver_locator = CaregiverLocator.objects.get(screening_identifier=maternal_dataset_obj.screening_identifier)
        except CaregiverLocator.DoesNotExist:
            caregiver_locator = mommy.make_recipe(
                'flourish_caregiver.caregiverlocator',
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,
                screening_identifier=maternal_dataset_obj.screening_identifier)

        worklist_cls = django_apps.get_model('flourish_follow.worklist')
        try:
            worklist_cls.objects.get(study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier)
        except worklist_cls.DoesNotExist:
            mommy.make_recipe(
                'flourish_follow.worklist',
                subject_identifier=None,
                study_maternal_identifier=caregiver_locator.study_maternal_identifier,)

        call = mommy.make_recipe(
            'flourish_follow.call',
            label='worklistfollowupmodelcaller')

        log = mommy.make_recipe(
            'flourish_follow.log',
            call=call,)

        mommy.make_recipe(
            'flourish_follow.logentry',
            log=log,
            study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,)
