from django import forms

from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin
from flourish_caregiver.models import TbReferral
from flourish_form_validations.form_validators.tb_referral_form_validator import \
    TbReferralFormValidator


class TbReferralForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = TbReferralFormValidator


    class Meta:
        model = TbReferral
        fields = '__all__'
