from django import forms
from django.apps import apps as django_apps
from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin
from flourish_caregiver.models.caregiver_tb_referral import TBReferralCaregiver
from flourish_child_validations.form_validators import ChildTBReferralFormValidator
from edc_constants.constants import YES
from flourish_caregiver.models.list_models import CaregiverTbReferralReasons


class CaregiverTBReferralForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = ChildTBReferralFormValidator
    tb_screening_model = 'flourish_caregiver.caregivertbscreening'

    @property
    def tb_screening_model_cls(self):
        return django_apps.get_model(self.tb_screening_model)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        maternal_visit = self.initial.get('maternal_visit', None)

        referral_reasons = []

        tb_screening_options = {
            'cough': 'cough_duration',
            'fever': 'fever_duration',
            'sweats': 'sweats_duration',
            'weight_loss': 'weight_loss_duration',
        }
        tb_screening_obj = self.tb_screening_model_cls.objects.filter(
            maternal_visit_id=maternal_visit).first()
        if tb_screening_obj:
            for symptom, duration in tb_screening_options.items():
                symptom_value = getattr(tb_screening_obj, symptom)
                duration_value = getattr(tb_screening_obj, duration)
                if symptom_value == YES and duration_value == '>= 2 weeks':
                    referral_reason = CaregiverTbReferralReasons.objects.filter(
                        short_name=symptom).first()
                    if referral_reason:
                        referral_reasons.append(referral_reason.id)
            if tb_screening_obj.household_diagnosed_with_tb == YES:
                referral_reason_other = CaregiverTbReferralReasons.objects.filter(
                    short_name='household_diagnosed_with_tb').first()
                if referral_reason_other:
                    referral_reasons.append(referral_reason_other.id)
        self.initial['reason_for_referral'] = referral_reasons

    class Meta:
        model = TBReferralCaregiver
        fields = '__all__'
