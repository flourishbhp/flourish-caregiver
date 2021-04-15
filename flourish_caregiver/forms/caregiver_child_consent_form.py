from django import forms

from ..models import CaregiverChildConsent
from .form_mixins import SubjectModelFormMixin

from flourish_form_validations.form_validators import CaregiverChildConsentFormValidator


class CaregiverChildConsentForm(SubjectModelFormMixin):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    study_child_identifier = forms.CharField(
        label='Previous study identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    form_validator_cls = CaregiverChildConsentFormValidator

    class Meta:
        model = CaregiverChildConsent
        fields = '__all__'
