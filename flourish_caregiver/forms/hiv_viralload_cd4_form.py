from django import forms

from flourish_form_validations.form_validators import HivViralLoadCd4FormValidator

from .form_mixins import SubjectModelFormMixin
from ..models import HivViralLoadAndCd4


class HivViralLoadCd4Form(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = HivViralLoadCd4FormValidator

    class Meta:
        model = HivViralLoadAndCd4
        fields = '__all__'
