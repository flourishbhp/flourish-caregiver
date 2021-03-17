from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from ..models import CaregiverPhqReferral


class CaregiverPhqReferralForm(SiteModelFormMixin, FormValidatorMixin,
                               forms.ModelForm):

    class Meta:
        model = CaregiverPhqReferral
        fields = '__all__'
