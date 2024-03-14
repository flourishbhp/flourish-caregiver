from django import forms
from edc_constants.choices import YES_NO

from flourish_form_validations.form_validators import BreastMilkCRFFormValidator
from .form_mixins import SubjectModelFormMixin
from ..choices import EXP_COUNT_CHOICES, YES_RESOLVED_NO
from ..models.breast_milk_crfs import BreastMilk6Months, BreastMilkBirth


class BreastMilkBirthForms(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = BreastMilkCRFFormValidator
    exp_mastitis = forms.ChoiceField(
        label='Since the mother started breastfeeding, has she experienced mastitis?',
        choices=YES_RESOLVED_NO,
        widget=forms.RadioSelect,

    )

    exp_mastitis_count = forms.ChoiceField(
        label='How many times has the participant experienced mastitis?',
        choices=EXP_COUNT_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

    exp_cracked_nipples = forms.ChoiceField(
        label='Has the participant experienced cracked nipples?',
        choices=YES_NO,
        widget=forms.RadioSelect,
        required=False
    )

    class Meta:
        model = BreastMilkBirth
        fields = '__all__'


class BreastMilk6MonthsForms(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = BreastMilkCRFFormValidator
    class Meta:
        model = BreastMilk6Months
        fields = '__all__'
