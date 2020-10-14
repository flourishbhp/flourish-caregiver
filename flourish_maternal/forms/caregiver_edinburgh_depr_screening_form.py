from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverEdinburghDeprScreening


class CaregiverEdinburghDeprScreeningForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = CaregiverEdinburghDeprScreening
        fields = '__all__'
