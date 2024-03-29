from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import ScreeningPregWomen, ScreeningPregWomenInline


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


class ScreeningPregWomenInlineForm(SiteModelFormMixin, FormValidatorMixin,
                                   forms.ModelForm):
    form_validator_cls = None

    child_subject_identifier = forms.CharField(
        label='Child Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def clean(self):
        self.cleaned_data = super().clean()

    def has_changed(self):
        return True

    class Meta:
        model = ScreeningPregWomenInline
        fields = '__all__'
