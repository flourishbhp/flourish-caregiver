import pdb

from django.core.exceptions import ValidationError

from .form_mixins import SubjectModelFormMixin
from django import forms
from ..models import Covid19
from flourish_form_validations.form_validators import Covid19FormValidator
from edc_constants.constants import *

class Covid19Form(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = Covid19FormValidator

    def __init__(self, *args, **kwargs):
        super(Covid19Form, self).__init__(*args, **kwargs)

        subject_identifier = self.initial.get('subject_identifier', None)

        if not subject_identifier:
            return

        prev_instance = Covid19.objects \
                .filter(maternal_visit__appointment__subject_identifier=subject_identifier) \
                .order_by('-report_datetime') \
                .first()

        if prev_instance:
            self.initial['fully_vaccinated'] = prev_instance.fully_vaccinated
            self.initial['vaccination_type'] = prev_instance.vaccination_type
            self.initial['other_vaccination_type'] = prev_instance.other_vaccination_type
            self.initial['first_dose'] = prev_instance.first_dose
            self.initial['second_dose'] = prev_instance.second_dose

    class Meta:
        model = Covid19
        fields = '__all__'
