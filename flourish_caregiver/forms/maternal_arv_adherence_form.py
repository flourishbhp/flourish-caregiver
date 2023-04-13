from django import forms

from ..models import MaternalArvAdherence
from .form_mixins import SubjectModelFormMixin

from flourish_form_validations.form_validators import MaternalArvAdherenceFormValidator


class MaternalArvAdherenceForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = MaternalArvAdherenceFormValidator

    class Meta:
        model = MaternalArvAdherence
        fields = '__all__'
