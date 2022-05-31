from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import ScreenToTbStudy


class TbStudyScreeningForm(SubjectModelFormMixin, forms.ModelForm):
    class Meta:
        model = ScreenToTbStudy
        fields = '__all__'
