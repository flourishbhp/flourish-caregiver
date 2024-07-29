from django import forms

from flourish_form_validations.form_validators.childhood_lead_exposure_risk_form_validator import \
    ChildhoodLeadExposureRiskFormValidator
from .form_mixins import SubjectModelFormMixin
from ..models.childhood_lead_exposure_risk import ChildhoodLeadExposureRisk


class ChildhoodLeadExposureRiskForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = ChildhoodLeadExposureRiskFormValidator
    class Meta:
        model = ChildhoodLeadExposureRisk
        fields = '__all__'
