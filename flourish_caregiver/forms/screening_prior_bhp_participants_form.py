from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from flourish_form_validations.form_validators import ScreeningPriorBhpParticipantsFormValidator

from ..models import ScreeningPriorBhpParticipants


class ScreeningPriorBhpParticipantsForm(
        SiteModelFormMixin, FormValidatorMixin,
        forms.ModelForm):

    form_validator_cls = ScreeningPriorBhpParticipantsFormValidator

    study_child_identifier = forms.CharField(
        label='Study child Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = ScreeningPriorBhpParticipants
        fields = '__all__'
