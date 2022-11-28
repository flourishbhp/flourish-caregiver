from flourish_form_validations.form_validators import CaregiverReferralFUFormValidator

from ..models import CaregiverPhqPostReferral
from .form_mixins import SubjectModelFormMixin


class CaregiverPhqPostReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFUFormValidator

    class Meta:
        model = CaregiverPhqPostReferral
        fields = '__all__'
