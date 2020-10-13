from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import MaternalHuuPreEnrollment


class MaternalHuuPreEnrollmentForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = MaternalHuuPreEnrollment
        fields = '__all__'
