from django import forms

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
        if subject_identifier:
            for key in self.fields.keys():
                self.fields[key].disabled = True

    def has_changed(self):
        return True

    class Meta:
        model = CaregiverChildConsent
        fields = '__all__'
