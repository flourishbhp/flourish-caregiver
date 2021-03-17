from .form_mixins import SubjectModelFormMixin
from ..models import CaregiverEdinburghReferral

from flourish_form_validations.form_validators import CaregiverReferralFormValidator


class CaregiverEdinburghReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFormValidator

    class Meta:
        model = CaregiverEdinburghReferral
        fields = '__all__'
