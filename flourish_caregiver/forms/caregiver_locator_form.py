from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from flourish_form_validations.form_validators import CaregiverLocatorFormValidator

from ..models import CaregiverLocator
from ..models import SubjectConsent


class CaregiverLocatorForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = CaregiverLocatorFormValidator

    screening_identifier = forms.CharField(
        label='Eligibility Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    study_maternal_identifier = forms.CharField(
        label='Study Caregiver Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            subject_consented = SubjectConsent.objects.filter(subject_identifier=self.initial[
                'subject_identifier'])
            if subject_consented:
                self.initial['first_name'] = subject_consented.first().first_name
                self.initial['last_name'] = subject_consented.first().last_name
        except:
            pass

    class Meta:
        model = CaregiverLocator
        fields = '__all__'
