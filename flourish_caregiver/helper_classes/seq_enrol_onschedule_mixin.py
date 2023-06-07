from django.apps import apps as django_apps
from edc_base import get_utcnow
from edc_visit_schedule import site_visit_schedules

from schedule_dict import child_schedule_dict, schedule_dict


class SeqEnrolOnScheduleMixin:
    def put_caregiver_onschedule(self, schedule_type, child_count):
        """Put a caregiver on schedule.
        """
        # TODO evaluate cohort
        cohort = self.evaluated_cohort
        onschedule_model = next(iter(schedule_dict[cohort][schedule_type]))
        schedule_name = schedule_dict[cohort][schedule_type][onschedule_model][
            child_count]
        onschedule_model = f'flourish_caregiver.{onschedule_model}'
        self.put_on_schedule(onschedule_model=onschedule_model,
                             schedule_name=schedule_name)

    def put_child_onschedule(self, schedule_type):
        # TODO evaluate cohort
        cohort = self.evaluated_cohort
        onschedule_model = schedule_dict[cohort][schedule_type]['onschedule_model']
        schedule_name = child_schedule_dict[cohort][schedule_type]['name']
        onschedule_model = f'flourish_child.{onschedule_model}'
        self.put_on_schedule(onschedule_model=onschedule_model,
                             schedule_name=schedule_name)

    def put_on_schedule(self, onschedule_model, schedule_name):
        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model,
            name=schedule_name)
        schedule.put_on_schedule(
            subject_identifier=self.caregiver_subject_identifier,
            onschedule_datetime=get_utcnow(),
            schedule_name=schedule_name)

        self.update_onschedule_model(onschedule_model=onschedule_model,
                                     schedule=schedule, schedule_name=schedule_name)

    def update_onschedule_model(self, onschedule_model, schedule_name, schedule):
        # Update onschedule child identifier
        onschedule_model_cls = django_apps.get_model(onschedule_model)
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
