from flourish_form_validations.form_validators import CaregiverReferralFUFormValidator

from ..models import CaregiverHamdReferralFU
from .form_mixins import SubjectModelFormMixin


class CaregiverHamdReferralFUForm(SubjectModelFormMixin):

    form_validator_cls = CaregiverReferralFUFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['emo_support_type'].label = ('4. What kind of emotional support are you '
                                                 'receiving?')

    class Meta:
        model = CaregiverHamdReferralFU
        fields = '__all__'
