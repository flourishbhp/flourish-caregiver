from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_constants.constants import NO, YES
from edc_form_validators import FormValidatorMixin
from flourish_form_validations.form_validators import SubjectConsentFormValidator

from ..models import SubjectConsent


class SubjectConsentForm(SiteModelFormMixin, FormValidatorMixin,
                         forms.ModelForm):

    form_validator_cls = SubjectConsentFormValidator

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def clean(self):
        cleaned_data = super().clean()
        child_consent = cleaned_data.get('child_consent')
        caregiver_child_consent = self.data.get('caregiverchildconsent_set-TOTAL_FORMS')

        if child_consent == NO and int(caregiver_child_consent) != 0:
            msg = {'child_consent':
                   'Participant is not willing to consent on behalf of child.'
                   'Caregiver child consent should not be completed. '}
            raise forms.ValidationError(msg)
        elif (child_consent == YES and int(caregiver_child_consent) == 0)\
                or not self.data.get('caregiverchildconsent_set-0-first_name'):
            raise forms.ValidationError('Please complete the Caregiver '
                                        'consent for child participation')

    class Meta:
        model = SubjectConsent
        fields = '__all__'
