from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import CaregiverSafiStigma


class CaregiverSafiStigmaForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = CaregiverSafiStigma
        fields = '__all__'
