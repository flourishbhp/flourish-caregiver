from django import forms
from flourish_form_validations.form_validators import TbKnowledgeFormValidator
from ..models import TbKnowledge
from .form_mixins import SubjectModelFormMixin


class TbKnowledgeForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = TbKnowledgeFormValidator

    class Meta:
        model = TbKnowledge
        fields = '__all__'
