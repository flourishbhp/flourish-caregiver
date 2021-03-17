from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from ..models import CaregiverGadReferral


class CaregiverGadReferralForm(SiteModelFormMixin, FormValidatorMixin,
                               forms.ModelForm):

    class Meta:
        model = CaregiverGadReferral
        fields = '__all__'
