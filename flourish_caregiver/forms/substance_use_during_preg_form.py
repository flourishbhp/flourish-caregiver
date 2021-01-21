from django import forms
# from flourish_form_validations.form_validators import SubstanceUseDuringPregFormValidator

from ..models import SubstanceUseDuringPregnancy
from .form_mixins import SubjectModelFormMixin


class SubstanceUseDuringPregnancyForm(SubjectModelFormMixin, forms.ModelForm):

#     form_validator_cls = SubstanceUseDuringPregFormValidator

    class Meta:
        model = SubstanceUseDuringPregnancy
        fields = '__all__'
