from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin
from flourish_caregiver.models.caregiver_tb_screening import CaregiverTBScreening
from flourish_child.forms import PreviousResultsFormMixin
from flourish_form_validations.form_validators.caregiver_tb_screening_form_validator import \
    CaregiverTBScreeningFormValidator


class CaregiverTBScreeningForm(PreviousResultsFormMixin, SubjectModelFormMixin):
    form_validator_cls = CaregiverTBScreeningFormValidator

    def get_keys_before(self, dict):
        key_stop = "maternal_visit"
        return_list = []
        for key in dict:
            if key == key_stop:
                break
            return_list.append(key)
        return return_list

    class Meta:
        model = CaregiverTBScreening
        fields = '__all__'
