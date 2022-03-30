from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from flourish_form_validations.form_validators import AntenatalEnrollmentFormValidator

from ..models import AntenatalEnrollment


class AntenatalEnrollmentForm(
        SiteModelFormMixin, FormValidatorMixin,
        forms.ModelForm):

    form_validator_cls = AntenatalEnrollmentFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        rapid_test_result = self.cleaned_data.get('rapid_test_result')
        rapid_test_date = self.cleaned_data.get('rapid_test_date')
        if self.instance.rapid_test_result and rapid_test_result:
            if rapid_test_result != self.instance.rapid_test_result:
                raise ValidationError(
                    'The rapid test result cannot be changed')
        if self.instance.rapid_test_date and rapid_test_date:
            if rapid_test_date != self.instance.rapid_test_date:
                raise ValidationError(
                    'The rapid test result date cannot be changed')
        self.validate_child_consent_exists()
        super().clean()

    def validate_child_consent_exists(self):
        child_consent_cls = django_apps.get_model('flourish_caregiver.caregiverchildconsent')

        child_consents = child_consent_cls.objects.filter(
            subject_identifier__startswith=self.cleaned_data.get('subject_identifier'),
            preg_enroll=True).order_by('consent_datetime')

        if not child_consents:
            raise forms.ValidationError(
                'Missing matching Child Subject Consent form, cannot proceed...')

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
