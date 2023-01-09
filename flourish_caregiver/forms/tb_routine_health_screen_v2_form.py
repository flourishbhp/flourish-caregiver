from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from flourish_form_validations.form_validators import TbRoutineHealthScreenV2FormValidator

from ..models import TbRoutineHealthScreenV2, TbRoutineHealthEncounters, MaternalVisit
from .form_mixins import SubjectModelFormMixin, InlineSubjectModelFormMixin
from ..choices import YES_NO_UNK_DWTA, VISIT_NUMBER


class TbRoutineHealthScreenV2Form(SubjectModelFormMixin, forms.ModelForm):
    tb_routine_health_screen_v2_model = 'flourish_caregiver.tbroutinehealthscreenv2'

    @property
    def tb_routine_health_screen_v2_cls(self):
        return django_apps.get_model(self.tb_routine_health_screen_v2_model)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        maternal_visit = self.initial.get('maternal_visit', None)
        # get current instance
        current_instance = self.tb_routine_health_screen_v2_cls.objects.filter(
            maternal_visit=maternal_visit).order_by(
            '-report_datetime').first()

        if current_instance:
            # get visit code
            vist_code = django_apps.get_model('flourish_caregiver.maternalvisit').objects.get(
                id=current_instance.maternal_visit_id).visit_code
            # if subject on enrollment visit change question to (since you became pregnant).
            if vist_code == '2000D':
                self.fields['tb_health_visits'] = forms.CharField(
                    label='How many health visits have you had since you became pregnant?',
                    widget=forms.RadioSelect(choices=VISIT_NUMBER))

    def clean(self):
        super().clean()

        total_inlines = int(self.data.get('routine_encounter-TOTAL_FORMS'), 0)

        tb_health_visit_number = int(self.cleaned_data.get('tb_health_visits'), 0)

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

    class Meta:
        model = TbRoutineHealthEncounters
        fields = '__all__'
