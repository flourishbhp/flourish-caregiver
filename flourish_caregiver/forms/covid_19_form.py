from .form_mixins import SubjectModelFormMixin
from django import forms
from ..models import Covid19
from flourish_form_validations.form_validators import Covid9FormValidator


class Covid19Form(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = Covid9FormValidator

    class Meta:
        model = Covid19
        fields = '__all__'
