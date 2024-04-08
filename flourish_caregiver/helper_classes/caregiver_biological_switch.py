from django.apps import apps as django_apps
from django.db.models import Q
from django.db.utils import IntegrityError
from edc_appointment.constants import NEW_APPT
from edc_constants.constants import OTHER, FEMALE

from .onschedule_helper import OnScheduleHelper
from ..identifiers import ScreeningIdentifier
from .utils import set_initials


class CaregiverBiologicalSwitch:
    """ Switch caregiver to enroll child with biological mother.
        Steps:
        1. Take caregiver offstudy
        2. Generate screening identifier for biological mother and update the relevant forms
            to associate to mother.
        3. Complete locator, screening for biological mother.
        4. Consent (w version) the biological mother on to the study, ensure pid matches
            caregiver pid.
        5. Associate caregiver consent on behalf of child with biological mother consent.
        6. Update child registered subject to associate with biological mother.
        7. Complete previously enrolled information form.
        8. Put mother on enrolment schedule.
        9. Put mother on quarterly schedule, begin where caregiver left off and
            align window periods for appointments.
    """

    def __init__(self, caregiver_sid=None):
        # Create new screening identifier to associate with the biological mother.
        self.screening_identifier = ScreeningIdentifier().identifier
        self.biological_mother_locator = None
        self.biological_mother_consent = None

        self.caregiver_sid = caregiver_sid

    @property
    def caregiver_offstudy_cls(self):
        return django_apps.get_model('flourish_prn.caregiveroffstudy')

    @property
    def registered_subject_cls(self):
        return django_apps.get_model('edc_registration.registeredsubject')

    @property
    def caregiver_locator_cls(self):
        return django_apps.get_model('flourish_caregiver.caregiverlocator')

    @property
    def maternal_dataset_cls(self):
        return django_apps.get_model('flourish_caregiver.maternaldataset')

    @property
    def screening_prior_cls(self):
        return django_apps.get_model('flourish_caregiver.screeningpriorbhpparticipants')

    @property
    def subject_consent_cls(self):
        return django_apps.get_model('flourish_caregiver.subjectconsent')

    @property
    def caregiverchild_consent_cls(self):
        return django_apps.get_model('flourish_caregiver.caregiverchildconsent')

    @property
    def caregiver_prev_enrolled_cls(self):
        return django_apps.get_model('flourish_caregiver.caregiverpreviouslyenrolled')

    @property
    def appointment_model_cls(self):
        return django_apps.get_model('edc_appointment.appointment')

    @property
    def child_appointment_cls(self):
        return django_apps.get_model('flourish_child.appointment')

    @property
    def child_visit_cls(self):
        return django_apps.get_model('flourish_child.childvisit')

    @property
    def caregiver_locator_obj(self):
        try:
            locator = self.caregiver_locator_cls.objects.get(
                subject_identifier=self.caregiver_sid)
        except self.caregiver_locator_cls.DoesNotExist:
            return None
        else:
            return locator

    @property
    def maternal_dataset_obj(self):
        try:
            dataset = self.maternal_dataset_cls.objects.get(
                study_maternal_identifier=self.caregiver_locator_obj.study_maternal_identifier)
        except self.maternal_dataset_cls.DoesNotExist:
            return None
        else:
            return dataset

    def take_caregiver_offstudy(self, report_dt=None, offstudy_dt=None,
                                reason='', reason_othr=None, offstudy_point=None,
                                comments=None):
        offstudy_defaults = {'report_datetime': report_dt,
                             'offstudy_date': offstudy_dt,
                             'reason': reason,
                             'offstudy_point': offstudy_point,
                             'comment': comments}
        if reason == OTHER:
            offstudy_defaults.update({'reason_other': reason_othr})
        obj, created = self.caregiver_offstudy_cls.objects.get_or_create(
            subject_identifier=self.caregiver_sid,
            defaults=offstudy_defaults, )

        if not created:
            obj.save()
        return True

    def update_dataset_screening_identifier(self, dataset_obj=None):
        dataset_obj.screening_identifier = self.screening_identifier
        dataset_obj.save()

    def create_bio_mother_locator(self, report_dt=None, signed_dt=None, **kwargs):
        dataset_obj = self.maternal_dataset_obj
        first_name = kwargs.get('first_name', dataset_obj.first_name)
        last_name = kwargs.get('last_name', dataset_obj.last_name)

        locator_defaults = {'screening_identifier': self.screening_identifier,
                            'study_maternal_identifier': dataset_obj.study_maternal_identifier,
                            'report_datetime': report_dt,
                            'locator_date': signed_dt,
                            'first_name': first_name,
                            'last_name': last_name}

        self.update_dataset_screening_identifier(dataset_obj)

        try:
            locator = self.caregiver_locator_cls.objects.create(
                **locator_defaults)
        except IntegrityError:
            raise Exception
        else:
            self.biological_mother_locator = locator

    def create_bio_screening(self, report_dt=None, **kwargs):
        dataset_obj = self.maternal_dataset_obj

        prior_screening_defaults = {
            'study_maternal_identifier': dataset_obj.study_maternal_identifier,
            'report_datetime': report_dt,
            **kwargs, }

        obj, created = self.screening_prior_cls.objects.get_or_create(
            screening_identifier=self.screening_identifier,
            defaults=prior_screening_defaults)

        if not created:
            print('This screening already exists, check it before proceeding')
        return obj

    def create_bio_consent(self, sid_swap=('C', 'B'), **kwargs):
        """ Create an instance of the subject consent for the participant.
            @param subject_type: Whether bioloigical mother or caregiver to determine sID.
            @param sid_swap: Tuple to determine the pid replacement pattern.
        """
        first_name = kwargs.pop(
            'first_name', self.biological_mother_locator.first_name)
        last_name = kwargs.pop(
            'last_name', self.biological_mother_locator.last_name)
        initials = set_initials(first_name, last_name)

        subject_identifier = self.caregiver_sid.replace(
            sid_swap[0], sid_swap[1])

        consent_defaults = {
            'subject_identifier': subject_identifier,
            'screening_identifier': self.screening_identifier,
            'first_name': first_name.upper() if first_name else None,
            'last_name': last_name.upper() if last_name else None,
            'initials': initials,
            'gender': FEMALE,
            **kwargs, }
        try:
            consent = self.subject_consent_cls.objects.create(
                **consent_defaults)
        except IntegrityError:
            raise Exception
        else:
            self.biological_mother_consent = consent

    def add_child_consent_to_mother(self):
        """ Add the caregiver consent on behalf of the child to the biological
            mother's consent, this will remove/disassociate it with the caregiver's consent.
        """
        child_consents = self.caregiverchild_consent_cls.objects.filter(
            subject_identifier__startswith=self.caregiver_sid)
        for consent in child_consents:
            self.biological_mother_consent.caregiverchildconsent_set.add(
                consent)

    def update_child_registered_subject(self):
        """ Update the relative identifier on the child's registered subject model
            object to associate with the biological mother's sID.
        """
        try:
            child_consent = self.biological_mother_consent.caregiverchildconsent_set.latest(
                'consent_datetime')
            registered_obj = self.registered_subject_cls.objects.get(
                subject_identifier=child_consent.subject_identifier)
        except (self.caregiverchild_consent_cls.DoesNotExist,
                self.registered_subject_cls.DoesNotExist):
            print(
                'Child consent was not moved correctly or Registered subject isn\'t there')
            raise Exception
        else:
            registered_obj.relative_identifier = self.biological_mother_consent.subject_identifier
            registered_obj.save()

    def create_bio_previous_enrol_info(self, report_dt=None, **kwargs):
        """ Create an instance of the caregiver previously enrolled form for the
            biological mother.
            @param report_dt: Date and time form captured.
            @return: instance of the caregiver previously enrolled object.
        """
        try:
            prev_enrol = self.caregiver_prev_enrolled_cls.objects.create(
                subject_identifier=self.biological_mother_consent.subject_identifier,
                report_datetime=report_dt,
                **kwargs)
        except IntegrityError:
            raise Exception
        else:
            return prev_enrol

    def put_on_enrol_schedule(self, onschedule_dt=None, base_appt_dt=None):
        instance = self.child_consent_model_obj
        subject_identifier = self.biological_mother_consent.subject_identifier
        helper_cls = self.instantiate_helper(
            subject_identifier, onschedule_dt, instance.cohort)
        helper_cls.put_cohort_onschedule(instance,
                                         base_appt_datetime=base_appt_dt or onschedule_dt)

    def put_on_quart_schedule(self, onschedule_dt=None, base_appt_dt=None):
        instance = self.child_consent_model_obj
        subject_identifier = self.biological_mother_consent.subject_identifier
        enrol_appt = self.appointment_model_cls.objects.filter(
            subject_identifier=subject_identifier).first()

        child_enrol_visit = self.child_visit_cls.objects.get(
            subject_identifier=instance.subject_identifier, visit_code='2000', visit_code_sequence=0)

        helper_cls = self.instantiate_helper(
            subject_identifier, onschedule_dt, instance.cohort)
        helper_cls.put_quarterly_onschedule(
            enrol_appt, base_appt_datetime=base_appt_dt or child_enrol_visit.report_datetime)

    def align_with_child_appts(self):
        instance = self.child_consent_model_obj
        complete_appts = self.child_appointment_cls.objects.filter(
            Q(schedule_name__icontains='quart') | Q(
                schedule_name__icontains='qt'),
            subject_identifier=instance.subject_identifier, ).exclude(
                appt_status=NEW_APPT).values_list('visit_code', flat=True).distinct()

        maternal_appts = [appt+'M' for appt in complete_appts]
        caregiver_appts = self.appointment_model_cls.objects.filter(
            subject_identifier=self.biological_mother_consent.subject_identifier,
            visit_code__in=maternal_appts)

        if caregiver_appts.exists():
            caregiver_appts.delete()

    @property
    def child_consent_model_obj(self):
        try:
            instance = self.biological_mother_consent.caregiverchildconsent_set.latest(
                'consent_datetime')
        except self.caregiverchild_consent_cls.DoesNotExist:
            print('Child consent was not moved correctly')
            raise Exception
        else:
            return instance

    def instantiate_helper(self, subject_identifier, onschedule_dt, cohort):
        onschedule_helper = OnScheduleHelper(
            subject_identifier=subject_identifier,
            onschedule_datetime=onschedule_dt,
            cohort=cohort)
        return onschedule_helper
