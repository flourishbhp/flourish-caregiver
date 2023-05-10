from django.apps import apps as django_apps
from edc_base.utils import get_utcnow
from edc_visit_schedule.site_visit_schedules import site_visit_schedules


class OnScheduleHelper(object):
    """A helper class that puts a participant into a particular schedule
    """

    def __init__(self, subject_identifier, onschedule_datetime=None, cohort=None, ):

        self.subject_identifier = subject_identifier
        self.onschedule_datetime = onschedule_datetime or get_utcnow()
        self.cohort = cohort

    def put_cohort_onschedule(self, instance, base_appt_datetime=None):
        if self.cohort is not None:
            if 'sec' in self.cohort:
                self.put_on_schedule(self.cohort,
                                     instance=instance,
                                     child_subject_identifier=instance.subject_identifier,
                                     base_appt_datetime=base_appt_datetime,
                                     caregiver_visit_count=instance.caregiver_visit_count)
            else:
                self.put_on_schedule((self.cohort + '_enrol'),
                                     instance=instance,
                                     child_subject_identifier=instance.subject_identifier,
                                     base_appt_datetime=base_appt_datetime,
                                     caregiver_visit_count=instance.caregiver_visit_count)

    def put_quarterly_onschedule(self, instance, base_appt_datetime=None):
        """ Determine the `cohort` and child count for multiple enrollments to
            enroll subject and call the put_on_schedule function to put the subject
            on a particular schedule.
            @param instance: object instance to determine cohort and count.
            @param base_appt_datetime: base datetime to start the appointment.
        """
        cohort = None
        if 'sec' in instance.schedule_name:
            cohort = '_'.join([self.cohort.rstrip('_sec'), 'sec_quart'])
        elif 'fu' in instance.schedule_name:
            cohort = '_'.join([self.cohort, 'fu_quarterly'])
        else:
            cohort = '_'.join([self.cohort, 'quarterly'])

        cohort_list = instance.schedule_name.split('_')
        caregiver_visit_count = cohort_list[1][-1:]

        onschedule_model = django_apps.get_model(instance.schedule.onschedule_model)

        child_subject_identifier = None

        try:
            onschedule_obj = onschedule_model.objects.get(
                subject_identifier=instance.subject_identifier,
                schedule_name=instance.schedule_name)
        except onschedule_model.DoesNotExist:
            raise
        else:
            child_subject_identifier = onschedule_obj.child_subject_identifier

        self.put_on_schedule(cohort,
                             instance=instance,
                             child_subject_identifier=child_subject_identifier,
                             base_appt_datetime=base_appt_datetime or instance.report_datetime.replace(
                                microsecond=0),
                             caregiver_visit_count=caregiver_visit_count)

    def put_on_schedule(self, cohort, instance=None, child_subject_identifier=None,
                        base_appt_datetime=None, caregiver_visit_count=None):

        subject_identifier = self.subject_identifier or instance.subject_consent.subject_identifier
        if instance:
            schedule, onschedule_model_cls, schedule_name = self.get_onschedule_model(
                cohort=cohort,
                caregiver_visit_count=caregiver_visit_count,
                instance=instance)

            assent_onschedule_datetime = self.get_assent_onschedule_datetime

            schedule.put_on_schedule(
                subject_identifier=subject_identifier,
                onschedule_datetime=(self.onschedule_datetime
                                     or assent_onschedule_datetime
                                     or instance.created.replace(microsecond=0)),
                schedule_name=schedule_name,
                base_appt_datetime=base_appt_datetime)

            try:
                onschedule_model_cls.objects.get(
                    subject_identifier=subject_identifier,
                    schedule_name=schedule_name,
                    child_subject_identifier=child_subject_identifier)
            except onschedule_model_cls.DoesNotExist:
                try:
                    onschedule_obj = schedule.onschedule_model_cls.objects.get(
                        subject_identifier=subject_identifier,
                        schedule_name=schedule_name,
                        child_subject_identifier='')
                except schedule.onschedule_model_cls.DoesNotExist:
                    pass
                else:
                    onschedule_obj.child_subject_identifier = (child_subject_identifier
                                                               or instance.subject_identifier)
                    onschedule_obj.save()

    def get_onschedule_model(self, cohort, caregiver_visit_count=None, instance=None):
        """ Retrieve the onschedule model, class and schedule name to enroll subject on.
            @param cohort: participant cohort name
            @param caregiver_visit_count: child count, for multi enrollment
            @param instance: `consent/appointment` instance
        """
        cohort_label_lower = ''.join(cohort.split('_'))

        if 'enrol' in cohort:
            cohort_label_lower = cohort_label_lower.replace('enrol', 'enrollment')

        onschedule_model = 'flourish_caregiver.onschedule' + cohort_label_lower

        children_count = str(self.get_schedule_sequence(
            instance,
            django_apps.get_model(onschedule_model),
            caregiver_visit_count=caregiver_visit_count))
        cohort = cohort + children_count

        if 'pool' not in cohort:
            cohort = cohort.replace('cohort_', '')

        schedule_name = cohort + '_schedule1'

        if 'tb_2_months' in cohort:
            onschedule_model = 'flourish_caregiver.onschedule' + cohort_label_lower
            schedule_name = 'tb_2_months_schedule'
        if 'tb_6_months' in cohort:
            onschedule_model = 'flourish_caregiver.onschedule' + cohort_label_lower
            schedule_name = 'tb_6_months_schedule'

        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model, name=schedule_name)

        onschedule_model_cls = django_apps.get_model(onschedule_model)

        return schedule, onschedule_model_cls, schedule_name

    @property
    def get_assent_onschedule_datetime(self):
        """ Get child assent object creation date to use as an onschedule datetime.
            @return: datetime created
        """
        child_assent_cls = django_apps.get_model('flourish_child.childassent')

        try:
            assent_obj = child_assent_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except child_assent_cls.DoesNotExist:
            return None
        else:
            return assent_obj.created.replace(microsecond=0)

    def get_schedule_sequence(self, instance, onschedule_cls, caregiver_visit_count=None):
        children_count = (caregiver_visit_count or
                          1 + onschedule_cls.objects.filter(
                              subject_identifier=self.subject_identifier).exclude(
                                  child_subject_identifier=instance.subject_identifier).count())
        return children_count
