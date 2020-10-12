from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import MaternalCyhuuPreEnrollment


class MaternalCyhuuPreEnrollmentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = MaternalCyhuuPreEnrollment
        fields = '__all__'
