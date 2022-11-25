from django import forms
from ..models import MaternalArvPostAdherence
from .form_mixins import SubjectModelFormMixin

from flourish_form_validations.form_validators import MaternalArvPostAdherenceFormValidator


class MaternalArvPostAdherenceForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = MaternalArvPostAdherenceFormValidator

    class Meta:
        model = MaternalArvPostAdherence
        fields = '__all__'
