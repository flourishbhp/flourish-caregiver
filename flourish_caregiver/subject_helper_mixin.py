from dateutil.relativedelta import relativedelta
from edc_appointment.models import Appointment
from edc_appointment.constants import COMPLETE_APPT
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from model_mommy import mommy


class SubjectHelperMixin:

    def get_maternal_dataset_options(self):
        options = {
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
            'protocol': '4',
            'site_name': 'Gaborone',
            'study_child_identifier': '056-4995621-1-10',
            'study_maternal_identifier': '056-49956',
            'toilet': 2,
            'toilet_indoors': 'Latrine or none',
            'toilet_private': 'Indoor toilet or private latrine'}
        return options

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

    def create_TD_enrollment(self, facility, **kwargs):
        import_holidays()


        mommy.make_recipe(
            'flourish_caregiver.screeningpriorbhpparticipants',)

        mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            **self.child_dataset_options)

        mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.get_maternal_dataset_options())

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            child_age_at_enrollment=get_utcnow() - relativedelta(years=2, months=5),
            ** self.options)

        return subject_consent.subject_identifier
