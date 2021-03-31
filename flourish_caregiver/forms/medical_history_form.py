from django import forms
from flourish_form_validations.form_validators import MedicalHistoryFormValidator

from .form_mixins import SubjectModelFormMixin
from ..models import MedicalHistory

from ..helper_classes import MaternalStatusHelper


class MedicalHistoryForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = MedicalHistoryFormValidator

    def clean(self):
        form_validator = self.form_validator_cls(
                    cleaned_data=self.cleaned_data)
        form_validator.subject_status = MaternalStatusHelper(
            maternal_visit=self.cleaned_data.get('maternal_visit')).hiv_status
        cleaned_data = form_validator.validate()
        return cleaned_data

    class Meta:
        model = MedicalHistory
        fields = '__all__'
