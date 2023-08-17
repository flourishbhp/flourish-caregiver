from itertools import chain

from django import forms
from django.db.models import ManyToManyField
from edc_base.sites import SiteModelFormMixin
from edc_constants.constants import YES
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
        required=False)

    last_name = forms.CharField(
        label='Last Name',
        required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            subject_consented = SubjectConsent.objects.filter(
                subject_identifier=self.initial.get('subject_identifier', None)).latest(
                'report_datetime')
        except SubjectConsent.DoesNotExist:
            pass
        else:
            self.fields['first_name'].widget = forms.TextInput(
                attrs={'readonly': 'readonly'})
            self.fields['last_name'].widget = forms.TextInput(
                attrs={'readonly': 'readonly'})
            self.initial['first_name'] = subject_consented.first_name
            self.initial['last_name'] = subject_consented.last_name

    def compare_instance_fields(self, prev_instance=None):
        exclude_fields = ['modified', 'created', 'user_created', 'user_modified',
                          'hostname_created', 'hostname_modified', 'device_created',
                          'device_modified', 'report_datetime', 'subject_identifier',
                          'is_locator_updated', 'action_identifier',
                          'tracking_identifier', 'related_tracking_identifier',
                          'parent_tracking_identifier', 'study_maternal_identifier',
                          'locator_date', 'may_sms'
                          ]
        if prev_instance:
            other_values = self.model_to_dict(prev_instance, exclude=exclude_fields)
            values = {key: self.data.get(key) or None for key in other_values.keys()}
            return values != other_values
        return False

    def model_to_dict(self, instance, exclude):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
            if not getattr(f, 'editable', False):
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, ManyToManyField):
                data[f.name] = [str(obj.id) for obj in f.value_from_object(instance)]
                continue
            data[f.name] = f.value_from_object(instance) or None
        return data

    def clean(self):
        self.cleaned_data = super().clean()
        subject_identifier = self.initial.get('subject_identifier', None)
        try:
            prev_instance = CaregiverLocator.objects.get(
                subject_identifier=subject_identifier)
        except CaregiverLocator.DoesNotExist:
            pass
        else:
            has_changed = self.compare_instance_fields(prev_instance)
            if not has_changed and self.cleaned_data.get('is_locator_updated') == YES:
                raise forms.ValidationError(
                    'No changes detected. Please update at least one field.')
        return self.cleaned_data

    class Meta:
        model = CaregiverLocator
        fields = '__all__'
