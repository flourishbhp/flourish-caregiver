from django import forms
from ..models import SubstanceUsePriorPregnancy
from .form_mixins import SubjectModelFormMixin


class SubstanceUsePriorPregnancyForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = None

    class Meta:
        model = SubstanceUsePriorPregnancy
        fields = '__all__'
