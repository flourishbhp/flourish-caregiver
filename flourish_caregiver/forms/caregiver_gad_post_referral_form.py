from flourish_form_validations.form_validators import CaregiverReferralFUFormValidator

from ..models import CaregiverGadPostReferral
from .form_mixins import SubjectModelFormMixin


class CaregiverGadPostReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFUFormValidator

    class Meta:
        model = CaregiverGadPostReferral
        fields = '__all__'
