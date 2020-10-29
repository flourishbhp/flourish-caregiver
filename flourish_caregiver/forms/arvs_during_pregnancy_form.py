from django import forms

from ..models import ArvsDuringPregnancy
from .form_mixins import SubjectModelFormMixin


class ArvsDuringPregnancyForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = ArvsDuringPregnancy
        fields = '__all__'
