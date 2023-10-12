from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from flourish_form_validations.form_validators import AntenatalEnrollmentFormValidator
from ..helper_classes import EnrollmentHelper

from ..models import AntenatalEnrollment


class AntenatalEnrollmentForm(
        SiteModelFormMixin, FormValidatorMixin,
        forms.ModelForm):

    form_validator_cls = AntenatalEnrollmentFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    child_consent_model = 'flourish_caregiver.caregiverchildconsent'

    @property
    def child_consent_cls(self):
        return django_apps.get_model(self.child_consent_model)
    @property
    def enrolment_helper_cls(self):
        return EnrollmentHelper

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

    def validate_maternal_hiv_status(self):
        """Validates maternal hiv status at enrollment."""
        enrollment_helper = self.enrolment_helper_cls(
            instance_antenatal=AntenatalEnrollment(**self.cleaned_data),
            exception_cls=forms.ValidationError)

        try:
            enrollment_helper.enrollment_hiv_status()
        except ValidationError:
            raise forms.ValidationError(
                'Unable to determine maternal hiv status at enrollment.')

        enrollment_helper.raise_validation_error_for_rapidtest()

    def validate_child_consent_exists(self):
        child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')

        child_consents = child_consent_cls.objects.filter(
            subject_consent__subject_identifier=self.cleaned_data.get('subject_identifier'),
            preg_enroll=True).order_by('consent_datetime')

        if not child_consents:
            raise forms.ValidationError(
                'Missing Child Consent associated with participant\'s '
                ' pregnancy screening form. Please correct.')

    class Meta:
        model = AntenatalEnrollment
        fields = '__all__'
