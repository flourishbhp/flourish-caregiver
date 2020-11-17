from django import forms

from ..models import MaternalDiagnoses
from .form_mixins import SubjectModelFormMixin


class MaternalDiagnosesForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = None

    class Meta:
        model = MaternalDiagnoses
        fields = '__all__'
