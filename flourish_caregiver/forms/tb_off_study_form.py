from django import forms
from edc_form_validators import FormValidatorMixin

from flourish_caregiver.models import TbOffStudy
from flourish_prn.form_validations import OffstudyFormValidator


class TbOffStudyForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = OffstudyFormValidator


    class Meta:
        model = TbOffStudy
        fields = '__all__'
