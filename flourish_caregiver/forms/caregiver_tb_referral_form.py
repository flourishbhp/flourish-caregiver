from django import forms

from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin
from flourish_caregiver.models.caregiver_tb_referral import TBReferralCaregiver
from flourish_child_validations.form_validators import ChildTBReferralFormValidator


class CaregiverTBReferralForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = ChildTBReferralFormValidator

    class Meta:
        model = TBReferralCaregiver
        fields = '__all__'
