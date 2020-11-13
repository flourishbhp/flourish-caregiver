from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import CaregiverLocator


class CaregiverLocatorForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    screening_identifier = forms.CharField(
        label='Eligibility Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    study_maternal_identifier = forms.CharField(
        label='Study Caregiver Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = CaregiverLocator
        fields = '__all__'
