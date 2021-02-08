from django import forms
from django.conf import settings

from edc_form_validators import FormValidatorMixin
from edc_base.sites import SiteModelFormMixin

from ..models import CaregiverChildConsent


class CaregiverChildConsentForm(SiteModelFormMixin, FormValidatorMixin,
                                forms.ModelForm):

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

    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = CaregiverChildConsent
        fields = '__all__'
