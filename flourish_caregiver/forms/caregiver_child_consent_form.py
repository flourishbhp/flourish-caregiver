from django import forms
from django.apps import apps as django_apps

from flourish_form_validations.form_validators import CaregiverChildConsentFormValidator

from ..models import CaregiverChildConsent
from .form_mixins import SubjectModelFormMixin


class CaregiverChildConsentForm(SubjectModelFormMixin):
    # form_validator_cls = CaregiverChildConsentFormValidator

    child_dataset_model = 'flourish_child.childdataset'

    @property
    def child_dataset_cls(self):
        return django_apps.get_model(self.child_dataset_model)

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    # first_name = forms.CharField(
        # label="First name",
        # widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        # required=False
    # )
    #
    # last_name = forms.CharField(
        # label="Last name",
        # widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        # required=False
    # )
    #
    # child_dob = forms.DateTimeField(
        # label="Date of birth",
        # widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        # required=False
    # )
    #
    # study_child_identifier = forms.CharField(
        # label="Previous Subject Identifier",
        # widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        # required=False
    # )
    #
    # gender = forms.CharField(
        # label="Gender",
        # widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        # required=False
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # # fields alread initialized in the super
        study_child_identifier = self.initial.get('study_child_identifier', None)
        gender = self.initial.get('gender', None)
        child_dob = self.initial.get('child_dob', None)

        self.fields['child_dob'].disabled = True
        # # if and only if the above fields exist, make the field readonly
        # # or else make the fields editable
        if study_child_identifier:
            self.fields['study_child_identifier'].disabled = True
        if gender:
            self.fields['gender'].disabled = True
        if child_dob:
            self.fields['child_dob'] = forms.CharField(
                initial=self.initial['child_dob'],)
            self.fields['child_dob'].disabled = True

        screening_identifier = kwargs.get('screening_identifier', None)
        setattr(CaregiverChildConsentFormValidator, 'screening', screening_identifier)

        instance = getattr(self, 'instance', None)
        subject_identifier = instance.subject_identifier if instance else None
        if subject_identifier and not self.screening_preg_exists(instance=instance):
            for key in self.fields.keys():
                self.fields[key].disabled = True
        self.errors

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
