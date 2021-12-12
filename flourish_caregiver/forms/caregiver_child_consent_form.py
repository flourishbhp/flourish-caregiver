from django import forms
from django.apps import apps as django_apps

from ..models import CaregiverChildConsent
from .form_mixins import SubjectModelFormMixin

from flourish_form_validations.form_validators import CaregiverChildConsentFormValidator


class CaregiverChildConsentForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverChildConsentFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        subject_identifier = instance.subject_identifier if instance else None
        if subject_identifier and not self.screening_preg_exists(instance=instance):
            for key in self.fields.keys():
                self.fields[key].disabled = True

    def has_changed(self):
        return True

    def screening_preg_exists(self, instance=None):
        preg_women_screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpregwomen')

        try:
            preg_women_screening_cls.objects.get(
                screening_identifier=instance.subject_consent.screening_identifier)
        except preg_women_screening_cls.DoesNotExist:
            return False
        else:
            return True

    class Meta:
        model = CaregiverChildConsent
        fields = '__all__'
