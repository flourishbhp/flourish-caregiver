import pdb

from .form_mixins import SubjectModelFormMixin
from django import forms
from ..models import Covid19
from flourish_form_validations.form_validators import Covid19FormValidator


class Covid19Form(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = Covid19FormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        subject_identifier = self.initial.get('subject_identifier', None)

        if subject_identifier:
            covid_instance = self._last_covid_instance(subject_identifier)

            self.initial['fully_vaccinated'] = covid_instance.fully_vaccinated
            self.initial['vaccination_type'] = covid_instance.vaccination_type
            self.initial['other_vaccination_type'] = covid_instance.other_vaccination_type
            self.initial['first_dose'] = covid_instance.first_dose
            self.initial['second_dose'] = covid_instance.second_dose



    def _last_covid_instance(self, subject_identifier):
        return Covid19.objects \
            .filter(maternal_visit__appointment__subject_identifier=subject_identifier) \
            .order_by('-report_datetime') \
            .first()

    class Meta:
        model = Covid19
        fields = '__all__'
