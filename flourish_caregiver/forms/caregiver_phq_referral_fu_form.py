from flourish_form_validations.form_validators import CaregiverReferralFUFormValidator

from ..models import CaregiverPhqReferralFU
from .form_mixins import SubjectModelFormMixin


class CaregiverPhqReferralFUForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFUFormValidator

    class Meta:
        model = CaregiverPhqReferralFU
        fields = '__all__'
