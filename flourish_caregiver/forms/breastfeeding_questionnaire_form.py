from django import forms
from ..models import BreastFeedingQuestionnaire
# from flourish_form_validations.form_validators import
from .form_mixins import SubjectModelFormMixin


class BreastFeedingQuestionnaireForm(SubjectModelFormMixin,forms.ModelForm):
    
    # form_validator_cls = 
    
    class Meta:
        model = BreastFeedingQuestionnaire
        fields = '__all__'
        