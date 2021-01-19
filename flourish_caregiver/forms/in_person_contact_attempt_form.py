from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import InPersonContactAttempt


class InPersonContactAttemptForm(
        SiteModelFormMixin, FormValidatorMixin,
        forms.ModelForm):

    study_maternal_identifier = forms.CharField(
        label='Study maternal Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = InPersonContactAttempt
        fields = '__all__'
