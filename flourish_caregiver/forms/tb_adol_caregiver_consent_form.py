from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from flourish_form_validations.form_validators import TbAdolConsentFormValidator

from edc_consent.modelform_mixins import ConsentModelFormMixin

from ..models import TbAdolConsent


class TbAdolConsentForm(SiteModelFormMixin, FormValidatorMixin,
                        ConsentModelFormMixin, forms.ModelForm):
    
    form_validator_cls = TbAdolConsentFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)
    
    def clean_guardian_and_dob(self):
        pass

    def clean_gender_of_consent(self):
        pass

    class Meta:
        model = TbAdolConsent
        fields = '__all__'
