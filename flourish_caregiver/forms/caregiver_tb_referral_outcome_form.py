from django import forms

from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin
from flourish_caregiver.models.caregiver_tb_referral_outcome import \
    CaregiverTBReferralOutcome
from flourish_form_validations.form_validators import \
    CaregiverTBReferralOutcomeFormValidator


class CaregiverTBReferralOutcomeForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = CaregiverTBReferralOutcomeFormValidator

    class Meta:
        model = CaregiverTBReferralOutcome
        fields = '__all__'
