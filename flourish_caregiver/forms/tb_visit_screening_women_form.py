from django import forms

from flourish_form_validations.form_validators import TbVisitScreeningWomenFormValidator
from .form_mixins import SubjectModelFormMixin
from ..models import TbVisitScreeningWomen


class TbVisitScreeningWomenForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = TbVisitScreeningWomenFormValidator

    class Meta:
        model = TbVisitScreeningWomen
        fields = '__all__'
