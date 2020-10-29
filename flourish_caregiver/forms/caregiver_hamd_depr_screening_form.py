from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverHamdDeprScreening


class CaregiverHamdDeprScreeningForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = CaregiverHamdDeprScreening
        fields = '__all__'
