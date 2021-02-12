from django import forms
from flourish_form_validations.form_validators import FoodSecurityQuestionnaireFormValidator

from ..models import FoodSecurityQuestionnaire
from .form_mixins import SubjectModelFormMixin


class FoodSecurityQuestionnaireForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = FoodSecurityQuestionnaireFormValidator

    class Meta:
        model = FoodSecurityQuestionnaire
        fields = '__all__'
