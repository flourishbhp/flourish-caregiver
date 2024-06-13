from django import forms
from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverCageAid
from flourish_form_validations.form_validators import CaregiverCageAidFormValidator


class CaregiverCageAidForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = CaregiverCageAidFormValidator

    class Meta:
        model = CaregiverCageAid
        fields = '__all__'
