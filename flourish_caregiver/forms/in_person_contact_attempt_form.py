from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from flourish_form_validations.form_validators import InPersonContactAttemptFormValidator
from ..models import InPersonContactAttempt


class InPersonContactAttemptForm(
        SiteModelFormMixin, FormValidatorMixin,
        forms.ModelForm):

    form_validator_cls = InPersonContactAttemptFormValidator

    study_maternal_identifier = forms.CharField(
        label='Study maternal Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = InPersonContactAttempt
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = self.update_choices_vars(self.custom_choices)
        self.fields['contact_location'] = forms.MultipleChoiceField(
            label='Which location was used for contact?',
            widget=forms.CheckboxSelectMultiple, choices=choices)
        self.fields['successful_location'] = forms.MultipleChoiceField(
            label='Which location was used for contact?',
            widget=forms.CheckboxSelectMultiple, choices=choices)

    def update_choices_vars(self, choice_list=[]):
        new_choices = []
        for choices in choice_list:
            choices[0] = choices[0]
            new_choices.append(tuple(choices))
        return new_choices
