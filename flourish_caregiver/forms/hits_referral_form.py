from flourish_form_validations.form_validators import CaregiverReferralFormValidator

from .form_mixins import SubjectModelFormMixin
from ..models import HITSReferral


class HITSReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFormValidator

    class Meta:
        model = HITSReferral
        fields = '__all__'
