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

    def has_changed(self):
        return True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        clean_data = super().clean()

        tb_healthvisit_inlines = int(self.data.get(
            'tbroutinehealthencounters_set-TOTAL_FORMS', 0))

        try:
            tb_health_visits_counter = int(clean_data.get('tb_health_visits'))
        except ValueError:
            pass
        else:
            if tb_healthvisit_inlines != tb_health_visits_counter:
                raise ValidationError(
                    {'tb_health_visits': 'Not equal to the provided number of visits'})

        return clean_data

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
