from django import forms

from ..models import ArvsPrePregnancy
from .form_mixins import SubjectModelFormMixin


class ArvsPrePregnancyForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = ArvsPrePregnancy
        fields = '__all__'
