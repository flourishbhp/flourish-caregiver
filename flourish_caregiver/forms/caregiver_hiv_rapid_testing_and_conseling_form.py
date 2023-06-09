from flourish_form_validations.form_validators import CaregiverReferralFUFormValidator

from ..models import CaregiverHivRapidTestAndConseling
from .form_mixins import SubjectModelFormMixin


class CaregiverHivRapidTestAndConselingForm(SubjectModelFormMixin):

    # form_validator_cls = #TODO

    class Meta:
        model = CaregiverHivRapidTestAndConseling
        fields = '__all__'
