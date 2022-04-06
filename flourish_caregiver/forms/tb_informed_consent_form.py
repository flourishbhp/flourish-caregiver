from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_consent.modelform_mixins import ConsentModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import TbInformedConsent


class TbInformedConsentForm(SiteModelFormMixin, FormValidatorMixin,
                            ConsentModelFormMixin, forms.ModelForm):
    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def clean_guardian_and_dob(self):
        pass


    class Meta:
        model = TbInformedConsent
        fields = '__all__'
