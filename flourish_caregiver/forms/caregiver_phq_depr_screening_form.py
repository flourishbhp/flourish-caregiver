from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverPhqDeprScreening


class CaregiverPhqDeprScreeningForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = CaregiverPhqDeprScreening
        fields = '__all__'
