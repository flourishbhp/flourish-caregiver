from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import ScreeningPregWomen


class ScreeningPregWomenForm(SiteModelFormMixin, FormValidatorMixin,
                             forms.ModelForm):

    form_validator_cls = None

    screening_identifier = forms.CharField(
        required=False,
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = ScreeningPregWomen
        fields = '__all__'
