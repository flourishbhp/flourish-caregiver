from django.test import TestCase, tag
from django.utils.datastructures import MultiValueDict
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES, NO, POS
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from dateutil.relativedelta import relativedelta

from ..forms import MedicalHistoryForm
from ..models import MaternalVisit, MedicalHistory
from ..models.list_models import WcsDxAdult, ChronicConditions
from ..subject_helper_mixin import SubjectHelperMixin


@tag('mh')
class TestMedicalHistoryForm(TestCase):

    def setUp(self):
        import_holidays()

        subject_identifier = '12345678'
        study_maternal_identifier = '89721'

        self.subject_identifier = subject_identifier[:-1] + '4'

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=16, months=4),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': study_maternal_identifier,
            'protocol': 'Mashi',
            'preg_pi': 1}

        self.child_dataset_options = {
            'infant_hiv_exposed': 'exposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': study_maternal_identifier,
            'study_child_identifier': '1234'}

        self.options = {
            'subject_identifier': self.subject_identifier,
            'consent_datetime': get_utcnow(),
            'version': '1'}

        child_dataset = mommy.make_recipe(
            'flourish_child.childdataset',
            subject_identifier=self.subject_identifier + '10',
            dob=get_utcnow() - relativedelta(years=16, months=4),
            **self.child_dataset_options)

        maternal_dataset_obj = mommy.make_recipe(
            'flourish_caregiver.maternaldataset',
            subject_identifier=self.subject_identifier,
            **self.maternal_dataset_options)

        sh = SubjectHelperMixin()

        sh.enroll_prior_participant_assent(
            maternal_dataset_obj.screening_identifier,
            child_dataset.study_child_identifier)

        mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(visit_code='2000M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        visit2000M = MaternalVisit.objects.get(visit_code='2000M')

        mommy.make_recipe(
            'flourish_caregiver.hivrapidtestcounseling',
            maternal_visit=visit2000M,
            result=POS)

        who = WcsDxAdult.objects.create(name=NOT_APPLICABLE, short_name='N/A')
        chronic_conditions = ChronicConditions.objects.create(
            name='Asthma', short_name='Asthma')

        self.medical_history_options = {'chronic_since': YES,
                                        'who_diagnosis': YES,
                                        'current_illness': YES,
                                        'current_symptoms': 'cough',
                                        'know_hiv_status': 'Nobody', }

        self.mh_visit2000M = MedicalHistory.objects.create(
            maternal_visit=visit2000M,
            **self.medical_history_options)
        self.mh_visit2000M.who.add(who)
        self.mh_visit2000M.caregiver_chronic.add(chronic_conditions)

        self.visit2001M = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(visit_code='2001M'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

    def test_medhistory_has_changed_invalid(self):
        """ Assert form not valid if medical history information
            has changed, but not indicated on the field
            `med_history_changed` i.e. NO
        """
        ChronicConditions.objects.create(
            name='Hypertension', short_name='Hypertension')
        medical_history_dict = MultiValueDict()
        medical_history_dict.update(
            **self.medical_history_options,
            report_datetime=get_utcnow(),
            maternal_visit=self.visit2001M,
            med_history_changed=NO, )
        for obj in ChronicConditions.objects.all():
            medical_history_dict.update(
                caregiver_chronic=str(obj.id))

        mh = MedicalHistoryForm(data=medical_history_dict)
        mh.previous_instance = self.mh_visit2000M
        self.assertFalse(mh.is_valid())

    @tag('tmhcv')
    def test_medhistory_has_changed_valid(self):
        """ Assert form valid if medical history information
            remains the same,and indicated on the field
            `med_history_changed` i.e. NO
        """
        medical_history_dict = MultiValueDict()
        medical_history_dict.update(
            **self.medical_history_options,
            report_datetime=get_utcnow(),
            maternal_visit=self.visit2001M,
            symptoms_start_date=get_utcnow(),
            clinic_visit=YES,
            med_history_changed=YES, )
        for obj in ChronicConditions.objects.all():
            medical_history_dict.update(
                caregiver_chronic=str(obj.id))
        for obj in WcsDxAdult.objects.all():
            medical_history_dict.update(
                who=str(obj.id))
        mh = MedicalHistoryForm(data=medical_history_dict)
        mh.previous_instance = self.mh_visit2000M
        self.assertTrue(mh.is_valid(), mh.errors)
