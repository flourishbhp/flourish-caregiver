from django import forms
from django.apps import apps as django_apps
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        subject_identifier = instance.subject_identifier if instance else None
        if subject_identifier:
            for key in self.fields.keys():
                self.fields[key].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        child_consent = cleaned_data.get('child_consent')
        caregiver_child_consent = self.data.get(
            'caregiverchildconsent_set-TOTAL_FORMS')

        if child_consent == NO and int(caregiver_child_consent) != 0:
            msg = {'child_consent':
                       'Participant is not willing to consent on behalf of child.'
                       'Caregiver child consent should not be completed. To proceed,'
                       ' close Caregiver Child Consent.'}

            raise forms.ValidationError(msg)
        elif child_consent == YES and int(caregiver_child_consent) == 0:

            raise forms.ValidationError('Please complete the Caregiver '
                                        'consent for child participation')

        self.validate_screening_done(int(caregiver_child_consent))

    def validate_screening_done(self, child_count):
        """Validate that screening is done before consent."""
        screening_model_cls = django_apps.get_model(
            'flourish_caregiver.screeningpregwomen')
        count = 0
        subject_identifiers = []
        for x in range(int(child_count)):
            study_child_identifier = self.data.get(
                f'caregiverchildconsent_set-{x}-study_child_identifier')

            _subject_identifier = self.data.get(
                f'caregiverchildconsent_set-{x}-subject_identifier'
            )

            if (study_child_identifier == '' and
                    _subject_identifier not in subject_identifiers):
                subject_identifiers.append(_subject_identifier)
                count += 1

        if count > 0:
            try:
                screening_obj = screening_model_cls.objects.get(
                    screening_identifier=self.cleaned_data.get('screening_identifier'))
            except screening_model_cls.DoesNotExist:
                pass
            else:
                screening_cont = screening_obj.screeningpregwomeninline_set.count()
                if screening_cont == 0:
                    raise forms.ValidationError('Screening not done. Cannot proceed.')
                elif screening_cont < count:
                    raise forms.ValidationError('Screening not done for all children. '
                                                'Cannot proceed.')

    class Meta:
        model = SubjectConsent
        fields = '__all__'
