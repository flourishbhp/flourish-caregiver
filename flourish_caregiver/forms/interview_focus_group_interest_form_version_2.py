from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import InterviewFocusGroupInterestV2
from flourish_form_validations.form_validators import InterviewFocusGroupInterestVersion2FormValidator


class InterviewFocusGroupInterestVersion2Form(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = InterviewFocusGroupInterestVersion2FormValidator

    class Meta:
        model = InterviewFocusGroupInterestV2
        fields = '__all__'

