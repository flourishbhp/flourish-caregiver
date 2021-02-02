from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import MaternalDiagnoses


class MaternalDiagnosesForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = MaternalDiagnoses
        fields = '__all__'
