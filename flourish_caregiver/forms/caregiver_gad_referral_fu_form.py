from flourish_form_validations.form_validators import CaregiverReferralFUFormValidator

from ..models import CaregiverGadReferralFU
from .form_mixins import SubjectModelFormMixin


class CaregiverGadReferralFUForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFUFormValidator

    class Meta:
        model = CaregiverGadReferralFU
        fields = '__all__'
