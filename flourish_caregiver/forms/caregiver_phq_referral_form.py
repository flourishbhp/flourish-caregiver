from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverPhqReferral

from flourish_form_validations.form_validators import CaregiverReferralFormValidator


class CaregiverPhqReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFormValidator

    class Meta:
        model = CaregiverPhqReferral
        fields = '__all__'
