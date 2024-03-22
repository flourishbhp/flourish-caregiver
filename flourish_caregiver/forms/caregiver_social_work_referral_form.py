from django import forms
from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverSocialWorkReferral
from flourish_form_validations.form_validators import CaregiverSocialWorkReferralFormValidator


class CaregiverSocialWorkReferralForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = CaregiverSocialWorkReferralFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['referral_for'].disabled = True

    class Meta:
        model = CaregiverSocialWorkReferral
        fields = '__all__'
