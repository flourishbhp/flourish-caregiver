from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import Enrollment


class EnrollmentForm(SiteModelFormMixin, FormValidatorMixin,
                     forms.ModelForm):

    class Meta:
        model = Enrollment
        fields = '__all__'
