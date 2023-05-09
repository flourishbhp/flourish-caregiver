from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import InterviewFocusGroupInterest
from flourish_form_validations.form_validators import InterviewFocusGroupInterestFormValidator


class InterviewFocusGroupInterestForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = InterviewFocusGroupInterestFormValidator

    class Meta:
        model = InterviewFocusGroupInterest
        fields = '__all__'

