from django import forms
from flourish_form_validations.form_validators import SubstanceUsePriorFormValidator

from ..models import SubstanceUsePriorPregnancy
from .form_mixins import SubjectModelFormMixin


class SubstanceUsePriorPregnancyForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = SubstanceUsePriorFormValidator

    class Meta:
        model = SubstanceUsePriorPregnancy
        fields = '__all__'
