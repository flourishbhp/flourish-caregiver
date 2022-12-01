from flourish_form_validations.form_validators import CaregiverReferralFUFormValidator

from ..models import CaregiverEdinburghReferralFU
from .form_mixins import SubjectModelFormMixin


class CaregiverEdinburghReferralFUForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFUFormValidator

    class Meta:
        model = CaregiverEdinburghReferralFU
        fields = '__all__'
