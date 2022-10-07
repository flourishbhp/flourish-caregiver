from django import forms
from ..models import TbInterviewTranscription
from .form_mixins import SubjectModelFormMixin


class TbInterviewTranscriptionForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = TbInterviewTranscription
        fields = '__all__'
