from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import TbStudyEligibility


class TbStudyScreeningForm(SubjectModelFormMixin, forms.ModelForm):
    class Meta:
        model = TbStudyEligibility
        fields = '__all__'
