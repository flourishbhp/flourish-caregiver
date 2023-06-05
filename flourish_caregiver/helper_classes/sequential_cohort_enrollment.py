from django.apps import apps as django_apps
from edc_constants.date_constants import timezone
from edc_base.utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules

from .cohort import Cohort
from ..models import (
    AntenatalEnrollment, CaregiverPreviouslyEnrolled,
    CaregiverChildConsent, OnScheduleCohortBFU, OnScheduleCohortAFU,
    OnScheduleCohortAFUQuarterly, OnScheduleCohortAQuarterly,
    OnScheduleCohortBFUQuarterly, OnScheduleCohortBQuarterly,
    OnScheduleCohortCFUQuarterly, OnScheduleCohortCQuarterly,
    OnScheduleCohortASecQuart, OnScheduleCohortBSecQuart,
    CaregiverOffSchedule)


class SequentialCohortEnrollmentError(Exception):
    pass


class SequentialCohortEnrollment:

    """Class that checks and enrols participants to the next
    the next cohort when they age up.
    """

    def __init__(self, child_subject_identifier=None):
        
        self.child_subject_identifier = child_subject_identifier
    
    @property
    def caregiver_subject_identifier(self):
        """Return child caregiver subject identifier.
        """
        registration_mdl_cls = django_apps.get_model('edc_registration', 'registeredsubject')
        try:
            registered_subject = registration_mdl_cls.objects.get(
                subject_identifier=self.child_subject_identifier)
        except registration_mdl_cls.DoesNotExist:
            return None
        else:
            registered_subject.relative_identifier
        return None


    def check_enrollment(self):
        """Return True if the child is enrolled.
        """
        enrolled = False
        try:
            AntenatalEnrollment.objects.get(
                subject_identifier=self.caregiver_subject_identifier)
        except AntenatalEnrollment.DoesNotExist:
            enrolled = False
        else:
            enrolled = True

        try:
            CaregiverPreviouslyEnrolled.objects.get(
                subject_idetifier=self.caregiver_subject_identifier)
        except CaregiverPreviouslyEnrolled.DoesNotExist:
            enrolled = False
        else:
            enrolled = True
        return enrolled
    
    @property
    def enrollment_cohort(self):
        """Returns the cohort the child was enrolled on the first time.
        """
        cohort = None
        try:
            cohort =  Cohort.objects.get(
                subject_identifier=self.child_subject_identifier)
        except Cohort.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f"The subject: {self.child_subject_identifier} does not "
                "have an enrollment cohort")
        else:
            cohort = cohort.name
        return cohort

    @property
    def child_current_age(self):
        try:
            caregiver_child_consent =  CaregiverChildConsent.objects.get(
                study_child_identifier=self.child_subject_identifier)
        except CaregiverChildConsent.DoesNotExist:
            raise SequentialCohortEnrollmentError(
                f"The subject: {self.child_subject_identifier} does not "
                "have a caregiver child consent")
        else:
            dob = caregiver_child_consent.child_dob
            age = Cohort(
                child_dob=dob,
                enrollment_date=timezone.now().date())
            return age
        return None

    @property
    def aged_up(self):
        """Return true if the child has aged up on the cohort
        they are currently enrolled on
        """
        if self.current_cohort == 'cohort_a':
            if self.child_current_age >= 5:
                return True
        elif self.current_cohort == 'cohort_b':
            if self.child_current_age > 10:
                True
        return False
    
    @property
    def current_cohort(self):
        """Returns the cohort the child was enrolled on the first time.
        """
        cohort = Cohort.objects.objects(
            suject_identifier=self.child_subject_identifier).order_by(
                'assign_datetime'
            )
        if cohort:
            return cohort.name
        return None

    @property
    def evaluated_cohort(self):
        """Return cohort name evaluated now.
        """
        return None

    def schedule_name(self, cohort):
        """ Build and return schedule name to enroll subject on.
            @param cohort: participant cohort name
            @param caregiver_visit_count: child count, for multi enrollment
        """
        child_count = ''
        caregiver_child_consent =  CaregiverChildConsent.objects.filter(
            study_child_identifier=self.child_subject_identifier).last()
        if caregiver_child_consent:
            child_count = caregiver_child_consent.caregiver_visit_count

        cohort_label_lower = ''.join(cohort.split('_'))

        if 'enrol' in cohort:
            cohort_label_lower = cohort_label_lower.replace('enrol', 'enrollment')

        onschedule_model = 'flourish_caregiver.onschedule' + cohort_label_lower

        cohort = cohort + str(caregiver_visit_count)

        if 'pool' not in cohort:
            cohort = cohort.replace('cohort_', '')

        schedule_name = cohort + '_schedule1'

        if 'tb_2_months' in cohort:
            schedule_name = f'a_tb{child_count}_2_months_schedule1'
        if 'tb_6_months' in cohort:
            schedule_name = f'a_tb{child_count}_6_months_schedule1'
        
        return schedule_name, onschedule_model

    @property
    def enroll_on_age_up_cohort(self):
        """Enroll a participant on new aged up cohort.
        """
        if self.aged_up and self.current_cohort != self.evaluated_cohort:
            # put them on a new aged up cohort
            try:
                Cohort.objects.get(
                    name=self.evaluated_cohort,
                    subject_identifier=self.child_subject_identifier)
            except Cohort.DoesNotExist:
                pass
            else:
                Cohort.objects.create(
                    subject_identifier=instance.study_child_identifier,
                    name=self.evaluated_cohort,
                    enrollment_cohort=False)
        # Put them offschedule

        # put them on the new cohort schedule
        schedule_name, onschedule_model = self.schedule_name(cohort=self.evaluated_cohort)
        else:
            _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                onschedule_model=onschedule_model,
                name=schedule_name)
            schedule.put_on_schedule(
            subject_identifier=self.caregiver_subject_identifier,
            onschedule_datetime= get_utcnow(),
            schedule_name=schedule_name,
            base_appt_datetime=base_appt_datetime)

            # Update onschedule caregiver identifier
            try:
                onschedule_model_cls.objects.get(
                    subject_identifier=self.caregiver_subject_identifier,
                    schedule_name=schedule_name,
                    child_subject_identifier=self.child_subject_identifier)
            except onschedule_model_cls.DoesNotExist:
                try:
                    onschedule_obj = schedule.onschedule_model_cls.objects.get(
                        subject_identifier=self.caregiver_subject_identifier,
                        schedule_name=schedule_name,
                        child_subject_identifier='')
                except schedule.onschedule_model_cls.DoesNotExist:
                    pass
                else:
                    onschedule_obj.child_subject_identifier = self.child_subject_identifier
                    onschedule_obj.save()

    @property
    def take_off_schedule(self):
        """Take participant off schedule from previous age cohort.
        """
        a_onschedule_models = [
            OnScheduleCohortAFUQuarterly,
            OnScheduleCohortAQuarterly,
        ]
        b_onschedule_models = [
            OnScheduleCohortBFUQuarterly,
            OnScheduleCohortBQuarterly,
        ]
        if self.enrollment_cohort == 'cohort_a' and self.aged_up:
            for onschedule_model in a_onschedule_models:
                if onschedule_model == OnScheduleCohortAFUQuarterly:
                    try:
                        OnScheduleCohortAFU.objects.get(
                         subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier
                        )
                    except OnScheduleCohortAFU.DoesNotExist:
                        pass
                    else:
                        try:
                            onschedule_obj = onschedule_model.objects.get(
                                subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier)
                        except onschedule_model.DoesNotExist:
                            pass
                        else:
                            #put offschedule
                            _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                                onschedule_model=onschedule_model._meta.label_lower,
                                name=onschedule_obj.schedule_name)
                            if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                                  report_datetime=get_utcnow()):
                                CaregiverOffSchedule.objects.create(
                                    schedule_name=onschedule_obj.schedule_name,
                                    subject_identifier=self.caregiver_subject_identifier
                                )
                else:
                    try:
                        onschedule_obj = onschedule_model.objects.get(
                            subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier)
                    except onschedule_model.DoesNotExist:
                        pass
                    else:
                        #put offschedule
                        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                            onschedule_model=onschedule_model._meta.label_lower,
                            name=onschedule_obj.schedule_name)
                        if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                                report_datetime=get_utcnow()):
                            CaregiverOffSchedule.objects.create(
                                schedule_name=onschedule_obj.schedule_name,
                                subject_identifier=self.caregiver_subject_identifier
                            )
        elif self.enrollment_cohort == 'cohort_b' and self.aged_up:
            for onschedule_model in b_onschedule_models:
                if onschedule_model == OnScheduleCohortBFUQuarterly:
                    try:
                        OnScheduleCohortBFU.objects.get(
                         subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier   
                        )
                    except OnScheduleCohortBFU.DoesNotExist:
                        pass
                    else:
                        try:
                            onschedule_obj = onschedule_model.objects.get(
                                subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier)
                        except onschedule_model.DoesNotExist:
                            pass
                        else:
                            #put offschedule
                            _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                                onschedule_model=onschedule_model._meta.label_lower,
                                name=onschedule_obj.schedule_name)
                            if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                                  report_datetime=get_utcnow()):
                                CaregiverOffSchedule.objects.create(
                                    schedule_name=onschedule_obj.schedule_name,
                                    subject_identifier=self.caregiver_subject_identifier
                                )
                else:
                    try:
                        onschedule_obj = onschedule_model.objects.get(
                            subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier)
                    except onschedule_model.DoesNotExist:
                        pass
                    else:
                        #put offschedule
                        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                            onschedule_model=onschedule_model._meta.label_lower,
                            name=onschedule_obj.schedule_name)
                        if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                                report_datetime=get_utcnow()):
                            CaregiverOffSchedule.objects.create(
                                schedule_name=onschedule_obj.schedule_name,
                                subject_identifier=self.caregiver_subject_identifier
                            )
        elif self.enrollment_cohort == 'cohort_sec_a' and self.aged_up:
            try:
                onschedule_obj = OnScheduleCohortASecQuart.objects.get(
                    subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier)
            except OnScheduleCohortASecQuart.DoesNotExist:
                pass
            else:
                #put offschedule
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=onschedule_model._meta.label_lower,
                    name=onschedule_obj.schedule_name)
                if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                        report_datetime=get_utcnow()):
                    CaregiverOffSchedule.objects.create(
                        schedule_name=onschedule_obj.schedule_name,
                        subject_identifier=self.caregiver_subject_identifier
                    )
        elif self.enrollment_cohort == 'cohort_sec_b' and self.aged_up:
            try:
                onschedule_obj = OnScheduleCohortBSecQuart.objects.get(
                    subject_identifier=self.caregiver_subject_identifier,
                         child_subject_identifier=self.child_subject_identifier)
            except OnScheduleCohortBSecQuart.DoesNotExist:
                pass
            else:
                #put offschedule
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=onschedule_model._meta.label_lower,
                    name=onschedule_obj.schedule_name)
                if schedule.is_onschedule(subject_identifier=self.caregiver_subject_identifier,
                        report_datetime=get_utcnow()):
                    CaregiverOffSchedule.objects.create(
                        schedule_name=onschedule_obj.schedule_name,
                        subject_identifier=self.caregiver_subject_identifier
                    )