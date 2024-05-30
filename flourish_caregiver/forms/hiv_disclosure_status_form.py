from django import forms

from flourish_form_validations.form_validators import HIVDisclosureStatusFormValidator
from .form_mixins import SubjectModelFormMixin
from ..models import HIVDisclosureStatusA, HIVDisclosureStatusB, HIVDisclosureStatusC


class HIVDisclosureStatusFormMixin(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = HIVDisclosureStatusFormValidator

    associated_child_identifier = forms.CharField(
        label='Associated child identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        abstract = True


class HIVDisclosureStatusFormA(HIVDisclosureStatusFormMixin, forms.ModelForm):
    form_validator_cls = HIVDisclosureStatusFormValidator

    class Meta:
        model = HIVDisclosureStatusA
        fields = '__all__'


class HIVDisclosureStatusFormB(HIVDisclosureStatusFormMixin, forms.ModelForm):
    form_validator_cls = HIVDisclosureStatusFormValidator

    class Meta:
        model = HIVDisclosureStatusB
        fields = '__all__'


class HIVDisclosureStatusFormC(HIVDisclosureStatusFormMixin, forms.ModelForm):
    form_validator_cls = HIVDisclosureStatusFormValidator

    class Meta:
        model = HIVDisclosureStatusC
        fields = '__all__'
