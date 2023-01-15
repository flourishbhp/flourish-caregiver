from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from flourish_form_validations.form_validators import TbRoutineHealthScreenV2FormValidator

from ..models import TbRoutineHealthScreenV2, TbRoutineHealthEncounters
from .form_mixins import SubjectModelFormMixin, InlineSubjectModelFormMixin


class TbRoutineHealthScreenV2Form(SubjectModelFormMixin, forms.ModelForm):
    tb_routine_health_screen_v2_model = 'flourish_caregiver.tbroutinehealthscreenv2'

    @property
    def tb_routine_health_screen_v2_cls(self):
        return django_apps.get_model(self.tb_routine_health_screen_v2_model)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        total_inlines = int(self.data.get('routine_encounter-TOTAL_FORMS', 0))

        tb_health_visit_number = int(self.cleaned_data.get('tb_health_visits', 0))

        if tb_health_visit_number == 0 and total_inlines != 0:
            msg = {'tb_health_visits': 'if no health visits were made, end of CRF'}
            raise ValidationError(msg)
        elif tb_health_visit_number != total_inlines:
            msg = {
                'tb_health_visits':
                    'Complete follow up questions for each visit specified.'
            }
            raise ValidationError(msg)

    class Meta:
        model = TbRoutineHealthScreenV2
        fields = '__all__'


class TbRoutineHealthEncountersForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = TbRoutineHealthScreenV2FormValidator

    def has_changed(self):
        return True

    class Meta:
        model = TbRoutineHealthEncounters
        fields = '__all__'
