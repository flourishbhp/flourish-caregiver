from django import forms
from edc_form_validators import FormValidatorMixin
from flourish_form_validations.form_validators import CaregiverContactFormValidator

from ..models import CaregiverContact


class CaregiverContactForm(FormValidatorMixin, forms.ModelForm):

    form_validator_cls = CaregiverContactFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    study_name = forms.CharField(
        label='Study Name',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = CaregiverContact
        fields = '__all__'
