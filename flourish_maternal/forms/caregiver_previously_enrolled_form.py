from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import CaregiverPreviouslyEnrolled


class CaregiverPreviouslyEnrolledForm(
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    class Meta:
        model = CaregiverPreviouslyEnrolled
        fields = '__all__'
