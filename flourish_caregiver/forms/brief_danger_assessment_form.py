from django import forms

from flourish_form_validations.form_validators import BriefDangerAssessmentFormValidator
from .form_mixins import SubjectModelFormMixin
from ..models import BriefDangerAssessment


class BriefDangerAssessmentForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = BriefDangerAssessmentFormValidator

    class Meta:
        model = BriefDangerAssessment
        fields = '__all__'
