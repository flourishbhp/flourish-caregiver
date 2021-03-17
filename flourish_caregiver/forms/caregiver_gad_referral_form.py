from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverGadReferral

from flourish_form_validations.form_validators import CaregiverReferralFormValidator


class CaregiverGadReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFormValidator

    class Meta:
        model = CaregiverGadReferral
        fields = '__all__'
