from django import forms
from edc_form_validators import FormValidator

from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin
from flourish_caregiver.models import TbReferral


class TbReferralForm(SubjectModelFormMixin, FormValidator, forms.ModelForm):

    def clean(self):
        super().clean()

        self.validate_other_specify(
            field='referral_clinic',
            other_specify_field='referral_clinic_other'
        )


    class Meta:
        model = TbReferral
        fields = '__all__'
