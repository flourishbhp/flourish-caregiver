from django import forms

from flourish_form_validations.form_validators import CaregiverClinicalMeasurementsFormValidator

from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverClinicalMeasurements


class CaregiverClinicalMeasurementsForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = CaregiverClinicalMeasurementsFormValidator

    class Meta:
        model = CaregiverClinicalMeasurements
        fields = '__all__'
