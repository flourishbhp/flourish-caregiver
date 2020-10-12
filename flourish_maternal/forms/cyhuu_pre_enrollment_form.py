from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import CyhuuPreEnrollment


class CyhuuPreEnrollmentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = CyhuuPreEnrollment
        fields = '__all__'
