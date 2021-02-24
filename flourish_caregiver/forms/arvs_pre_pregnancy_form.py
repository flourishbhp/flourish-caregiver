from django import forms
from flourish_form_validations.form_validators import ArvsPrePregnancyFormValidator

from ..models import ArvsPrePregnancy
from .form_mixins import SubjectModelFormMixin


class ArvsPrePregnancyForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = ArvsPrePregnancyFormValidator

    class Meta:
        model = ArvsPrePregnancy
        fields = '__all__'
