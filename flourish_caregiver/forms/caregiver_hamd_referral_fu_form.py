from flourish_form_validations.form_validators import CaregiverReferralFUFormValidator

from ..models import CaregiverHamdReferralFU
from .form_mixins import SubjectModelFormMixin


class CaregiverHamdReferralFUForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFUFormValidator

    class Meta:
        model = CaregiverHamdReferralFU
        fields = '__all__'
