from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import SubjectScreening


class SubjectScreeningForm(SiteModelFormMixin, FormValidatorMixin,
                           forms.ModelForm):

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = SubjectScreening
        fields = '__all__'
