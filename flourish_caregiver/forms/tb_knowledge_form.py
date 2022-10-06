from django import forms

from ..models import TbKnowledge
from .form_mixins import SubjectModelFormMixin


class TbKnowledgeForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = TbKnowledge
        fields = '__all__'
