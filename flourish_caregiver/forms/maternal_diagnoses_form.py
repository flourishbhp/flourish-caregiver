from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import MaternalDiagnoses

from flourish_form_validations.form_validators import MaternalDiagnosesFormValidator


class MaternalDiagnosesForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = MaternalDiagnosesFormValidator

    class Meta:
        model = MaternalDiagnoses
        fields = '__all__'
