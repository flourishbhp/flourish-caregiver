from dateutil.relativedelta import relativedelta
from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from edc_appointment.constants import NEW_APPT
from edc_appointment.creators import AppointmentInProgressError
from edc_appointment.creators import InvalidParentAppointmentMissingVisitError
from edc_appointment.creators import InvalidParentAppointmentStatusError
from edc_appointment.creators import UnscheduledAppointmentCreator
from edc_appointment.creators import UnscheduledAppointmentError
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_APPLICABLE, YES
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from .models import CaregiverLocator, MaternalDataset


class SubjectHelperMixin:

    def __init__(self):
        self.options = None
        self.child_dataset_options = None
        self.maternal_dataset_options = None

    def create_cohort_c_dataset(self):

        self.maternal_dataset_options = {
            'delivdt': get_utcnow() - relativedelta(years=3, months=2),
            'mom_enrolldate': get_utcnow(),
            'mom_hivstatus': 'HIV-infected',
            'study_maternal_identifier': '8907-21',
            'protocol': 'Tshilo Dikotla'
        }

        self.child_dataset_options = {
            'infant_hiv_exposed': 'Unexposed',
            'infant_enrolldate': get_utcnow(),
            'study_maternal_identifier': '8907-21',
            'study_child_identifier': '1234'
        }

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
            'flourish_caregiver.screeningpregwomen', )

        self.options = {
            'consent_datetime': get_utcnow(),
            'screening_identifier': preg_screening.screening_identifier,
            'breastfeed_intent': YES,
            'version': kwargs.get('version', None) or '1'
        }

        subject_consent = mommy.make_recipe(
            'flourish_caregiver.subjectconsent',
            **self.options)

        child_consent = mommy.make_recipe(
            'flourish_caregiver.caregiverchildconsent',
            subject_consent=subject_consent,
            child_dob=None,
            first_name=None,
            last_name=None, )

        mommy.make_recipe(
            'flourish_caregiver.antenatalenrollment',
            subject_identifier=subject_consent.subject_identifier,
            child_subject_identifier=child_consent.subject_identifier,
        )

        mommy.make_recipe(
            'flourish_caregiver.caregiverlocator',
            subject_identifier=subject_consent.subject_identifier, )

        anc_visit = mommy.make_recipe(
            'flourish_caregiver.maternalvisit',
            appointment=Appointment.objects.get(
                visit_code='1000M',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'flourish_caregiver.ultrasound',
            maternal_visit=anc_visit,
            child_subject_identifier=child_consent.subject_identifier,
            number_of_gestations=1
        )

        return subject_consent.subject_identifier

    def create_TD_efv_enrollment(self, screening_identifier, study_child_identifier,
                                 **kwargs):
        import_holidays()

        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            mommy.make_recipe(
                'flourish_caregiver.flourishconsentversion',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                version='1',
                child_version='1')

            prior_screening = mommy.make_recipe(
                'flourish_caregiver.screeningpriorbhpparticipants',
                screening_identifier=maternal_dataset_obj.screening_identifier)

            consent_options = {
                'consent_datetime': get_utcnow(),
                'screening_identifier': prior_screening.screening_identifier,
                'breastfeed_intent': YES,
                'version': '1'
            }

            subject_consent = mommy.make_recipe(
                'flourish_caregiver.subjectconsent',
                **consent_options)

            mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                study_child_identifier=study_child_identifier,
                child_dob=maternal_dataset_obj.delivdt, )

            mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled')

            return subject_consent.subject_identifier
        return None

    def create_TD_no_hiv_enrollment(self, screening_identifier, study_child_identifier,
                                    **kwargs):
        import_holidays()

        self.maternal_dataset_options['mom_hivstatus'] = 'HIV-uninfected'

        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            mommy.make_recipe(
                'flourish_caregiver.flourishconsentversion',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                version='1',
                child_version='1')

            prior_screening = mommy.make_recipe(
                'flourish_caregiver.screeningpriorbhpparticipants',
                screening_identifier=maternal_dataset_obj.screening_identifier)

            consent_options = {
                'consent_datetime': get_utcnow(),
                'screening_identifier': prior_screening.screening_identifier,
                'breastfeed_intent': YES,
                'version': '1'
            }

            subject_consent = mommy.make_recipe(
                'flourish_caregiver.subjectconsent',
                **consent_options)

            mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                study_child_identifier=study_child_identifier,
                child_dob=maternal_dataset_obj.delivdt, )

            mommy.make_recipe(
                'flourish_caregiver.caregiverpreviouslyenrolled')

            return subject_consent.subject_identifier
        return None

    def prepare_prior_participant_enrollment(self, maternal_dataset_obj):
        try:
            caregiver_locator = CaregiverLocator.objects.get(
                study_maternal_identifier=maternal_dataset_obj
                .study_maternal_identifier, )
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
            call=call, )

        mommy.make_recipe(
            'flourish_follow.logentry',
            log=log,
            study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,
            user_created='flourish')
        return caregiver_locator

    def enroll_prior_participant(self, screening_identifier, study_child_identifier,
                                 hiv_status=None, version='1', child_version='1',
                                 options={}, child_consent_options={},
                                 update_created_dt=None):

        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            self.options = options or {
                'consent_datetime': get_utcnow(),
                'version': version}

            screening_options = {
                'child_alive': YES,
                'mother_alive': YES,
                'flourish_participation': 'interested'}

            mommy.make_recipe(
                'flourish_caregiver.flourishconsentversion',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                version=version,
                child_version=child_version)

            mommy.make_recipe(
                'flourish_caregiver.screeningpriorbhpparticipants',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,
                **screening_options)

            subject_consent = mommy.make_recipe(
                'flourish_caregiver.subjectconsent',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                breastfeed_intent=NOT_APPLICABLE,
                biological_caregiver=YES,
                **self.options)

            child_consent = mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                study_child_identifier=study_child_identifier,
                child_dob=maternal_dataset_obj.delivdt,
                **child_consent_options)

            if update_created_dt:
                subject_consent.created = self.options.get('consent_datetime')
                child_consent.created = child_consent_options.get('consent_datetime')
                subject_consent.save()
                child_consent.save()

            if hiv_status:
                mommy.make_recipe(
                    'flourish_caregiver.caregiverpreviouslyenrolled',
                    subject_identifier=subject_consent.subject_identifier,
                    current_hiv_status=hiv_status,
                    report_datetime=self.options.get('consent_datetime'))
            else:
                mommy.make_recipe(
                    'flourish_caregiver.caregiverpreviouslyenrolled',
                    subject_identifier=subject_consent.subject_identifier,
                    report_datetime=self.options.get('consent_datetime'))
            return subject_consent.subject_identifier

    def enroll_prior_participant_assent(self, screening_identifier,
                                        study_child_identifier,
                                        consent_datetime=None, hiv_status=None,
                                        bio_mother_options={}):
        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            self.options = {
                'consent_datetime': consent_datetime or get_utcnow(),
                'version': '1'
            }

            mommy.make_recipe(
                'flourish_caregiver.flourishconsentversion',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                version='1',
                child_version='1')

            mommy.make_recipe(
                'flourish_caregiver.screeningpriorbhpparticipants',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                study_maternal_identifier=maternal_dataset_obj.study_maternal_identifier,
                **bio_mother_options)

            subject_consent = mommy.make_recipe(
                'flourish_caregiver.subjectconsent',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                breastfeed_intent=NOT_APPLICABLE,
                **self.options)

            caregiver_child_consent_obj = mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                study_child_identifier=study_child_identifier,
                child_dob=maternal_dataset_obj.delivdt, )

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

            if hiv_status:
                mommy.make_recipe(
                    'flourish_caregiver.caregiverpreviouslyenrolled',
                    subject_identifier=subject_consent.subject_identifier,
                    current_hiv_status=hiv_status)
            else:
                mommy.make_recipe(
                    'flourish_caregiver.caregiverpreviouslyenrolled',
                    subject_identifier=subject_consent.subject_identifier)

            return subject_consent.subject_identifier

    def enroll_prior_participant_twins_assent(self, screening_identifier,
                                              study_child_identifier1,
                                              study_child_identifier2,
                                              consent_datetime=None,
                                              hiv_status=None
                                              ):

        try:
            maternal_dataset_obj = MaternalDataset.objects.get(
                screening_identifier=screening_identifier)
        except MaternalDataset.DoesNotExist:
            pass
        else:
            self.options = {
                'consent_datetime': consent_datetime or get_utcnow(),
                'version': '1'
            }

            mommy.make_recipe(
                'flourish_caregiver.flourishconsentversion',
                screening_identifier=maternal_dataset_obj.screening_identifier,
                version='1',
                child_version='1')

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
                study_child_identifier=study_child_identifier1,
                child_dob=maternal_dataset_obj.delivdt, )

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

            caregiver_child_consent_obj2 = mommy.make_recipe(
                'flourish_caregiver.caregiverchildconsent',
                subject_consent=subject_consent,
                study_child_identifier=study_child_identifier2,
                child_dob=maternal_dataset_obj.delivdt, )

            mommy.make_recipe(
                'flourish_child.childassent',
                subject_identifier=caregiver_child_consent_obj2.subject_identifier,
                first_name=caregiver_child_consent_obj2.first_name,
                last_name=caregiver_child_consent_obj2.last_name,
                dob=caregiver_child_consent_obj2.child_dob,
                identity=caregiver_child_consent_obj2.identity,
                confirm_identity=caregiver_child_consent_obj2.identity,
                remain_in_study=YES,
                version=subject_consent.version)

            if hiv_status:
                mommy.make_recipe(
                    'flourish_caregiver.caregiverpreviouslyenrolled',
                    subject_identifier=subject_consent.subject_identifier,
                    current_hiv_status=hiv_status)
            else:
                mommy.make_recipe(
                    'flourish_caregiver.caregiverpreviouslyenrolled',
                    subject_identifier=subject_consent.subject_identifier)

            return subject_consent.subject_identifier

    def create_unscheduled_appointment(self, base_appointment):

        unscheduled_appointment_cls = UnscheduledAppointmentCreator

        options = {
            'subject_identifier': base_appointment.subject_identifier,
            'visit_schedule_name': base_appointment.visit_schedule.name,
            'schedule_name': base_appointment.schedule.name,
            'visit_code': base_appointment.visit_code,
            'suggested_datetime': get_utcnow(),
            'check_appointment': False,
            'appt_status': NEW_APPT,
            'facility': base_appointment.facility
        }

        try:
            appoinment = unscheduled_appointment_cls(**options)
        except (ObjectDoesNotExist, UnscheduledAppointmentError,
                InvalidParentAppointmentMissingVisitError,
                InvalidParentAppointmentStatusError,
                AppointmentInProgressError) as e:
            raise ValidationError(str(e))
        else:
            return appoinment.appointment
