from flourish_form_validations.form_validators import CaregiverReferralFUFormValidator

from ..models import CaregiverHamdPostReferral
from .form_mixins import SubjectModelFormMixin


class CaregiverHamdPostReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFUFormValidator

    class Meta:
        model = CaregiverHamdPostReferral
        fields = '__all__'
