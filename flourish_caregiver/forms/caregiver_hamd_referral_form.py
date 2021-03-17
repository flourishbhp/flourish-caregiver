from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from ..models import CaregiverHamdReferral


class CaregiverHamdReferralForm(SiteModelFormMixin, FormValidatorMixin,
                               forms.ModelForm):

    class Meta:
        model = CaregiverHamdReferral
        fields = '__all__'
