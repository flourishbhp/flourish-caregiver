from django import forms

from ..models import FoodFrequencyQuestionnaire
from .form_mixins import SubjectModelFormMixin


class FoodFrequencyQuestionnaireForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = FoodFrequencyQuestionnaire
        fields = '__all__'
