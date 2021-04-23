from django import forms
from flourish_form_validations.form_validators import SocioDemographicDataFormValidator

from ..models import SocioDemographicData
from .form_mixins import SubjectModelFormMixin


class SocioDemographicDataForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = SocioDemographicDataFormValidator

    class Meta:
        model = SocioDemographicData
        fields = '__all__'
