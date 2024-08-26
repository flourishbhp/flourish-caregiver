from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin
from flourish_caregiver.models.caregiver_tb_screening import CaregiverTBScreening
from flourish_form_validations.form_validators.caregiver_tb_screening_form_validator import \
    CaregiverTBScreeningFormValidator


class CaregiverTBScreeningForm(SubjectModelFormMixin):
    form_validator_cls = CaregiverTBScreeningFormValidator

    class Meta:
        model = CaregiverTBScreening
        fields = '__all__'
