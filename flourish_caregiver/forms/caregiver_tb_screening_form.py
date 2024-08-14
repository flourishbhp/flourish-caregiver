from django import forms

from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin
from flourish_caregiver.models.caregiver_tb_screening import CaregiverTBScreening
from flourish_child.forms import PreviousResultsFormMixin
from flourish_form_validations.form_validators.caregiver_tb_screening_form_validator import \
    CaregiverTBScreeningFormValidator


class CaregiverTBScreeningForm(PreviousResultsFormMixin, SubjectModelFormMixin):
    form_validator_cls = CaregiverTBScreeningFormValidator

    @staticmethod
    def generate_forms_for_previous_instances(queryset):
        form_fields = {}
        for i, instance in enumerate(queryset):
            for fld in instance._meta.fields:
                form_fields[
                    f"instance_{instance.maternal_visit.visit_code}_{fld.name}"] = (
                    forms.ChoiceField(initial=getattr(instance, fld.name)))
        return form_fields

    class Meta:
        model = CaregiverTBScreening
        fields = '__all__'
