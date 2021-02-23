from django import forms
from flourish_form_validations.form_validators import ObstericalHistoryFormValidator

from ..models import ObstericalHistory
from .form_mixins import SubjectModelFormMixin


class ObstericalHistoryForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = ObstericalHistoryFormValidator

    class Meta:
        model = ObstericalHistory
        fields = '__all__'
