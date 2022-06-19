from django import forms
from ..models import BreastFeedingQuestionnaire
from flourish_form_validations.form_validators import BreastFeedingQuestionnaireFormValidator
from .form_mixins import SubjectModelFormMixin


class BreastFeedingQuestionnaireForm(SubjectModelFormMixin,forms.ModelForm):
    
    form_validator_cls = BreastFeedingQuestionnaireFormValidator
    
    class Meta:
        model = BreastFeedingQuestionnaire
        fields = '__all__'
        