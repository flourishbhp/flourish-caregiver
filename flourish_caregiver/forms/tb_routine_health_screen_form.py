from django import forms
from flourish_form_validations.form_validators import TbRoutineHealthScreenFormValidator

from ..models import TbRoutineHealthScreen
from .form_mixins import SubjectModelFormMixin


class TbRoutineHealthScreenForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = TbRoutineHealthScreenFormValidator

    class Meta:
        model = TbRoutineHealthScreen
        fields = '__all__'
