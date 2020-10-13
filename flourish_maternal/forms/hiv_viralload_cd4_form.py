from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import HivViralLoadAndCd4


class HivViralLoadCd4Form(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = HivViralLoadAndCd4
        fields = '__all__'
