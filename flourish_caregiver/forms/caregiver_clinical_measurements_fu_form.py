from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverClinicalMeasurementsFu


class CaregiverClinicalMeasurementsFuForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = CaregiverClinicalMeasurementsFu
        fields = '__all__'
