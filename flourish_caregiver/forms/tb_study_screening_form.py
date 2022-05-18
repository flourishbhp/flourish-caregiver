from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import TbStudyScreening


class TbStudyScreeningForm(SubjectModelFormMixin, forms.ModelForm):
    class Meta:
        model = TbStudyScreening
        fields = '__all__'
