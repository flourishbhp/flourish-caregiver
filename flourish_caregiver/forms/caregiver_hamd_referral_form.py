from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverHamdReferral

from flourish_form_validations.form_validators import CaregiverReferralFormValidator


class CaregiverHamdReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFormValidator

    class Meta:
        model = CaregiverHamdReferral
        fields = '__all__'
