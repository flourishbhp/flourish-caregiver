from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from flourish_form_validations.form_validators import TbRoutineHealthScreenV2FormValidator

from ..models import TbRoutineHealthScreenV2, TbRoutineHealthEncounters
from .form_mixins import SubjectModelFormMixin, InlineSubjectModelFormMixin
from ..choices import YES_NO_UNK_DWTA, VISIT_NUMBER


class TbRoutineHealthScreenV2Form(SubjectModelFormMixin, forms.ModelForm):
    tb_routine_health_screen_v2_model = 'flourish_caregiver.tbroutinehealthscreenv2'

    @property
    def tb_routine_health_screen_v2_cls(self):
        return django_apps.get_model(self.tb_routine_health_screen_v2_model)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        subject_identifier = self.initial.get('subject_identifier', None)
        # get previous appointment
        prev_instance = self.tb_routine_health_screen_v2_cls.objects.filter(
            maternal_visit__appointment__subject_identifier=subject_identifier).order_by(
            '-report_datetime').first()

        # if subject on first visit change question to (since you became pregnant).
        if not prev_instance:
            # if the previous instance exist, change the question
            self.fields['tb_health_visits'] = forms.CharField(
                label='How many health visits have you had since you became pregnant?',
                widget=forms.RadioSelect(choices=VISIT_NUMBER))

    def clean(self):
        super().clean()

        total_inlines = int(self.data.get('routine_encounter-TOTAL_FORMS'))

        tb_health_visit_number = int(self.cleaned_data.get('tb_health_visits'))

        if tb_health_visit_number == 0 and total_inlines != 0:
            msg = {'tb_health_visits': 'if no health visits were made, end of CRF'}
            raise ValidationError(msg)
        elif tb_health_visit_number >= 1 and total_inlines == 0:
            msg = {
                'tb_health_visits':
                    'Complete follow up questions for each visit specified.'
            }
            raise ValidationError(msg)


    class Meta:
        model = TbRoutineHealthScreenV2
        fields = '__all__'


class TbRoutineHealthEncountersForm(SubjectModelFormMixin,forms.ModelForm):
    form_validator_cls = TbRoutineHealthScreenV2FormValidator

    class Meta:
        model = TbRoutineHealthEncounters
        fields = '__all__'
