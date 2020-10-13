from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import HuuPreEnrollment


class HuuPreEnrollmentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = HuuPreEnrollment
        fields = '__all__'
