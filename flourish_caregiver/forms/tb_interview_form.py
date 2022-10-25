from django import forms

from flourish_form_validations.form_validators import TbInterviewFormValidator

from ..models import TbInterview
from .form_mixins import SubjectModelFormMixin


class TbInterviewForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = TbInterviewFormValidator

    class Meta:
        model = TbInterview
        fields = '__all__'
