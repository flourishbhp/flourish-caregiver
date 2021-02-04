from ..models import CaregiverReferral
from .form_mixins import SubjectModelFormMixin

from flourish_form_validations.form_validators import CaregiverReferralFormValidator


class CaregiverReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFormValidator

    class Meta:
        model = CaregiverReferral
        fields = '__all__'
