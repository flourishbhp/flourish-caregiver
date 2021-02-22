from django import forms
from ..models import MaternalInterimIdcc
from .form_mixins import SubjectModelFormMixin

from flourish_form_validations.form_validators import MaternalIterimIdccFormValidator


class MaternalInterimIdccForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = MaternalIterimIdccFormValidator

    class Meta:
        model = MaternalInterimIdcc
        fields = '__all__'
