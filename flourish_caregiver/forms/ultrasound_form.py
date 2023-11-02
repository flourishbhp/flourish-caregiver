from django import forms
from django.apps import apps as django_apps

from flourish_form_validations.form_validators import UltrasoundFormValidator
from .form_mixins import SubjectModelFormMixin
from ..load_cohort_schedules import flourish_schedules
from ..models import UltraSound


class UltraSoundForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = UltrasoundFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields['maternal_visit']._queryset.exists():
            child_subject_identifier = self.get_child_subject_identifier_by_visit(
                self.fields['maternal_visit']._queryset[0])
            self.fields['child_subject_identifier'].initial = child_subject_identifier
            self.fields['child_subject_identifier'].widget.attrs['readonly'] = True

    def get_child_subject_identifier_by_visit(self, visit):
        onschedule_model = next((schedule.get('onschedule_model') for schedule in
                                 flourish_schedules if schedule.get('schedule_name') ==
                                 visit.schedule_name), None)
        if onschedule_model:
            onschedule_model_cls = django_apps.get_model(
                onschedule_model)

            try:
                onschedule_obj = onschedule_model_cls.objects.get(
                    subject_identifier=visit.subject_identifier,
                    schedule_name=visit.schedule_name)
            except onschedule_model_cls.DoesNotExist:
                return None
            else:
                return onschedule_obj.child_subject_identifier

    class Meta:
        model = UltraSound
        fields = '__all__'
