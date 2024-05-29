from django import forms

from flourish_form_validations.form_validators import HIVDisclosureStatusFormValidator
from .form_mixins import SubjectModelFormMixin
from ..models import HIVDisclosureStatusA, HIVDisclosureStatusB, HIVDisclosureStatusC


class HIVDisclosureStatusFormMixin(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = HIVDisclosureStatusFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['associated_child_identifier'].initial = kwargs['initial'].get(
                'associated_child_identifier')
        elif self.instance and self.instance.pk:
            self.fields[
                'associated_child_identifier'].initial = (
                self.instance.associated_child_identifier)

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
