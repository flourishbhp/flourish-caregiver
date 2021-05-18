from django import forms
from flourish_form_validations.form_validators import SocioDemographicDataFormValidator

from ..models import SocioDemographicData
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
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    class Meta:
        model = SocioDemographicData
        fields = '__all__'
