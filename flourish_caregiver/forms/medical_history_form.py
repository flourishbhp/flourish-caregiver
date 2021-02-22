from django import forms
from flourish_form_validations.form_validators import MedicalHistoryFormValidator

from .form_mixins import SubjectModelFormMixin
from ..models import MedicalHistory


class MedicalHistoryForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = MedicalHistoryFormValidator

    class Meta:
        model = MedicalHistory
        fields = '__all__'
