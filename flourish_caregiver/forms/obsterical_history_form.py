from django import forms
from ..models import ObstericalHistory
from .form_mixins import SubjectModelFormMixin


class ObstericalHistoryForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = None

    class Meta:
        model = ObstericalHistory
        fields = '__all__'
