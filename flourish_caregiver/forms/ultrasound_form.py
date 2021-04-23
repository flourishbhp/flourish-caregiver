from django import forms
from ..models import UltraSound
from .form_mixins import SubjectModelFormMixin

from flourish_form_validations.form_validators import UltrasoundFormValidator


class UltraSoundForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = UltrasoundFormValidator

    class Meta:
        model = UltraSound
        fields = '__all__'
