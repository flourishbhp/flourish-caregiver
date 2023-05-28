from django import forms
from ..models import MaternalInterimIdccVersion2
from .form_mixins import SubjectModelFormMixin

from flourish_form_validations.form_validators import MaternalIterimIdccFormValidator


class MaternalInterimIdccFormVersion2(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = MaternalIterimIdccFormValidator

    class Meta:
        model = MaternalInterimIdccVersion2
        fields = '__all__'
