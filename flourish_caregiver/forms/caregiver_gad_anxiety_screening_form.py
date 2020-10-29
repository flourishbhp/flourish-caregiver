from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverGadAnxietyScreening


class CaregiverGadAnxietyScreeningForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = CaregiverGadAnxietyScreening
        fields = '__all__'
