from django import forms
from .form_mixins import SubjectModelFormMixin
from ..models import MaternalHivInterimHx

from flourish_form_validations.form_validators import MaternalHivInterimHxFormValidator


class MaternalHivInterimHxForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = MaternalHivInterimHxFormValidator

    class Meta:
        model = MaternalHivInterimHx
        fields = '__all__'
