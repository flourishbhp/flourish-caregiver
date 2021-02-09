from django import forms
from django.conf import settings

from edc_form_validators import FormValidatorMixin
from edc_base.sites import SiteModelFormMixin

from ..models import CaregiverChildConsent

from flourish_form_validations.form_validators import CaregiverChildConsentFormValidator


class CaregiverChildConsentForm(SiteModelFormMixin, FormValidatorMixin,
                                forms.ModelForm):

    form_validator_cls = CaregiverChildConsentFormValidator

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    language = forms.CharField(
        label='Language of consent',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    is_literate = forms.CharField(
        label='Is the participant literate?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    dob = forms.CharField(
        label='Date of birth',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    is_dob_estimated = forms.CharField(
        label='Is date of birth estimated?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    citizen = forms.CharField(
        label='Is the participant a Botswana citizen?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    identity = forms.CharField(
        label='Identity number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    identity_type = forms.CharField(
        label='What type of identity number is this?',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    confirm_identity = forms.CharField(
        label='Retype the identity number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = CaregiverChildConsent
        fields = '__all__'
