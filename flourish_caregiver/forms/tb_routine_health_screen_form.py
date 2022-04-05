from django import forms
from django.apps import apps as django_apps
from flourish_form_validations.form_validators import TbRoutineHealthScreenFormValidator

from ..models import TbRoutineHealthScreen
from .form_mixins import SubjectModelFormMixin
from ..choices import YES_NO_UNK_DWTA


class TbRoutineHealthScreenForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = TbRoutineHealthScreenFormValidator

    tb_routine_health_screen_model = 'flourish_caregiver.tbroutinehealthscreen'

    @property
    def tb_routine_health_screen_cls(self):
        return django_apps.get_model(self.tb_routine_health_screen_model)

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Get subject identifier to get records for a specifice crf
        # subject identifier is always prefilled
        subject_identifier = self.initial.get('subject_identifier', None)

        # Get all tb routine crfs and from that get the last saved
        # can never throw an exception throw an exception
        prev_instance = self.tb_routine_health_screen_cls.objects.filter(
            maternal_visit__appointment__subject_identifier=subject_identifier,).order_by(
                '-report_datetime').first()

        if prev_instance:
            # if the previous instance exist, change the question
            self.fields['tb_screened'] = forms.CharField(
                label='Were you screened for TB at a routine healthcare encounter '
                'with the four screening questions (cough for 2 weeks, '
                'fever, weight loss, night sweats) between enrolment and delivery?',
                widget=forms.RadioSelect(choices=YES_NO_UNK_DWTA))

    class Meta:
        model = TbRoutineHealthScreen
        fields = '__all__'
