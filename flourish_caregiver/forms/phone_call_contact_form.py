from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

from ..models import PhoneCallContact


class PhoneCallContactForm(
        SiteModelFormMixin, FormValidatorMixin,
        forms.ModelForm):

#     study_maternal_identifier = forms.CharField(
#         label='Study maternal Subject Identifier',
#         widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = PhoneCallContact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = self.update_choices_vars(self.custom_choices)
        self.fields['phone_num_type'] = forms.MultipleChoiceField(
            label='Which phone number(s) was used for contact?',
            widget=forms.CheckboxSelectMultiple, choices=choices)
        self.fields['phone_num_success'] = forms.MultipleChoiceField(
            label='Which number(s) were you successful in reaching?',
            widget=forms.CheckboxSelectMultiple, choices=choices)

    def update_choices_vars(self, choices_list=[]):
        new_choices = []
        for choices in choices_list:
            choices[0] = choices[0].removesuffix('_fail')
            new_choices.append(tuple(choices))
        return new_choices
