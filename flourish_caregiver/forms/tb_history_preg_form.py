from django import forms
from flourish_form_validations.form_validators import TbHistoryPregFormValidator

from ..models import TbHistoryPreg
from .form_mixins import SubjectModelFormMixin


class TbHistoryPregForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = TbHistoryPregFormValidator

    class Meta:
        model = TbHistoryPreg
        fields = '__all__'
