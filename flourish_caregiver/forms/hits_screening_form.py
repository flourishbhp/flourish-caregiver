from django import forms

from flourish_form_validations.form_validators.hits_screening_form_validator import \
    HITSScreeningFormValidator
from .form_mixins import SubjectModelFormMixin
from ..models import HITSScreening


class HITSScreeningForm(SubjectModelFormMixin, forms.ModelForm):
    score = forms.CharField(
        label='Total HITS Score',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    form_validator_cls = HITSScreeningFormValidator

    class Meta:
        model = HITSScreening
        fields = '__all__'
