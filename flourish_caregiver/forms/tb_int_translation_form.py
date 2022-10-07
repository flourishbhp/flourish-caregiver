from django import forms
from ..models import TbInterviewTranslation
from .form_mixins import SubjectModelFormMixin


class TbInterviewTranslationForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = TbInterviewTranslation
        fields = '__all__'
