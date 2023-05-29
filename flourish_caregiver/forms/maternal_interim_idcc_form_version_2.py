from django import forms
from ..models import MaternalInterimIdccVersion2
from .form_mixins import SubjectModelFormMixin

from flourish_form_validations.form_validators import MaternalIterimIdccFormVersion2Validator


class MaternalInterimIdccFormVersion2(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = MaternalIterimIdccFormVersion2Validator

    class Meta:
        model = MaternalInterimIdccVersion2
        fields = '__all__'
