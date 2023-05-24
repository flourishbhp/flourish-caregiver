from django import forms
from django.db.models import ManyToManyField
from edc_constants.constants import YES, NO, NOT_APPLICABLE
from flourish_form_validations.form_validators import SocioDemographicDataFormValidator
from itertools import chain
from ..models import SocioDemographicData, HouseHoldDetails
from .form_mixins import SubjectModelFormMixin


class SocioDemographicDataForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = SocioDemographicDataFormValidator

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        instance = kwargs.get('instance')
        previous_instance = getattr(self, 'previous_instance', None)

        if not instance and previous_instance:
            for key in self.base_fields.keys():
                if key not in ['maternal_visit', 'report_datetime']:
                    initial[key] = getattr(previous_instance, key)

            # Initialize expense_contributors field
            contributors = getattr(previous_instance, 'expense_contributors',
                                   None)
            if contributors:
                contributor_ids = contributors.values_list('id', flat=True)
                initial['expense_contributors'] = contributor_ids
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        previous_instance = getattr(self, 'previous_instance', None)
        has_changed = self.compare_instance_fields(previous_instance)
        socio_demo_changed = self.cleaned_data.get('socio_demo_changed')
        if socio_demo_changed:
            self.validate_med_history_changed(socio_demo_changed)
            if socio_demo_changed == YES and not has_changed:
                message = {'socio_demo_changed':
                               'Participant\'s Socio-demographic information has '
                               'changed since '
                               'last visit. Please update the information on this form.'}
                raise forms.ValidationError(message)
            elif socio_demo_changed == NO and has_changed:
                message = {'socio_demo_changed':
                               'Participant\'s Socio-demographic information has not '
                               'changed '
                               'since last visit. Please don\'t make any changes to '
                               'this form.'}
                raise forms.ValidationError(message)
        cleaned_data = super().clean()
        return cleaned_data

    def compare_instance_fields(self, prev_instance=None):
        exclude_fields = ['modified', 'created', 'user_created', 'user_modified',
                          'hostname_created', 'hostname_modified', 'device_created',
                          'device_modified', 'report_datetime', 'maternal_visit',
                          'socio_demo_changed', ]
        if prev_instance:
            other_values = self.model_to_dict(prev_instance, exclude=exclude_fields)
            values = {key: self.data.get(key) or None for key in other_values.keys()}
            return values != other_values
        return False

    def validate_med_history_changed(self, med_history_changed):
        if med_history_changed == NOT_APPLICABLE:
            msg = {'socio_demo_changed': 'This field is applicable.'}
            raise forms.ValidationError(msg)

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

    class Meta:
        model = SocioDemographicData
        fields = '__all__'


class HouseHoldDetailsForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = None

    child_identifier = forms.CharField(
        label='Child Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}), )

    def has_changed(self):
        return True

    class Meta:
        model = HouseHoldDetails
        fields = '__all__'
