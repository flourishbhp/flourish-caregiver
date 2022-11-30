from flourish_form_validations.form_validators import CaregiverReferralFUFormValidator

from ..models import CaregiverEdinburghPostReferral
from .form_mixins import SubjectModelFormMixin


class CaregiverEdinburghPostReferralForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFUFormValidator

    class Meta:
        model = CaregiverEdinburghPostReferral
        fields = '__all__'
