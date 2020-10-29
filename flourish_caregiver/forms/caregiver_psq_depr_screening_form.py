from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverPsqDeprScreening


class CaregiverPsqDeprScreeningForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = CaregiverPsqDeprScreening
        fields = '__all__'
