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
        caregiver_child_consent = self.data.get('caregiverchildconsent_set-TOTAL_FORMS')

        if child_consent == NO and int(caregiver_child_consent) != 0:
            msg = {'child_consent':
                   'Participant is not willing to consent on behalf of child.'
                   'Caregiver child consent should not be completed. To proceed,'
                   ' close Caregiver Child Consent.'}

            raise forms.ValidationError(msg)
        elif child_consent == YES and int(caregiver_child_consent) == 0:

            if not self.is_pregnant():
                raise forms.ValidationError('Please complete the Caregiver '
                                            'consent for child participation')

    def is_pregnant(self):
        screening_preg_cls = django_apps.get_model('flourish_caregiver.screeningpregwomen')

        try:
            screening_preg_cls.objects.get(
                screening_identifier=self.cleaned_data.get('screening_identifier'))
        except screening_preg_cls.DoesNotExist:
            return False
        else:
            if self.cleaned_data.get('subject_identifier'):
                delivery_cls = django_apps.get_model('flourish_caregiver.maternaldelivery')
                try:
                    delivery_cls.objects.get(
                        subject_identifier=self.cleaned_data.get('subject_identifier'))
                except delivery_cls.DoesNotExist:
                    return True
                else:
                    return False
            return True

    class Meta:
        model = SubjectConsent
        fields = '__all__'
