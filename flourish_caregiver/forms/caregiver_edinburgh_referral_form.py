from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from ..models import CaregiverEdinburghReferral


class CaregiverEdinburghReferralForm(SiteModelFormMixin, FormValidatorMixin,
                               forms.ModelForm):

    class Meta:
        model = CaregiverEdinburghReferral
        fields = '__all__'
