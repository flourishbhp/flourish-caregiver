from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import FlourishConsentVersion


class FlourishConsentVersionForm(SiteModelFormMixin, FormValidatorMixin,
                                 forms.ModelForm):

    class Meta:
        model = FlourishConsentVersion
        fields = '__all__'
