from django import forms
from flourish_form_validations.form_validators import TbScreenPregFormValidator

from ..models import TbScreenPreg
from .form_mixins import SubjectModelFormMixin


class TbScreenPregForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = TbScreenPregFormValidator

    class Meta:
        model = TbScreenPreg
        fields = '__all__'
