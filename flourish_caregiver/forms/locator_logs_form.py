from django import forms

from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from flourish_form_validations.form_validators import LocatorLogEntryFormValidator
from ..models import LocatorLog


class LocatorLogForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = LocatorLog
        fields = '__all__'
