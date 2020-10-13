from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import MedicalHistory


class MedicalHistoryForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = MedicalHistory
        fields = '__all__'
