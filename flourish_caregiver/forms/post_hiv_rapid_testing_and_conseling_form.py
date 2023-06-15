from flourish_form_validations.form_validators import CaregiverReferralFUFormValidator

from ..models import PostHivRapidTestAndConseling
from .form_mixins import SubjectModelFormMixin
from flourish_form_validations.form_validators import PostHIVRapidTestCounselingFormValidator


class PostHivRapidTestAndConselingForm(SubjectModelFormMixin):

    form_validator_cls = PostHIVRapidTestCounselingFormValidator

    class Meta:
        model = PostHivRapidTestAndConseling
        fields = '__all__'
