from django import forms
from .form_mixins import SubjectModelFormMixin
from ..models import MaternalHivInterimHx
from django.core.validators import RegexValidator

from flourish_form_validations.form_validators import MaternalHivInterimHxFormValidator


class MaternalHivInterimHxForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = MaternalHivInterimHxFormValidator

    vl_result = forms.CharField(
        validators=[RegexValidator(r'^[0-9]*$', 'Viral load can only be a number')],
        max_length=35)

    class Meta:
        model = MaternalHivInterimHx
        fields = '__all__'
