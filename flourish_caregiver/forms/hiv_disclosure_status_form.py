from django import forms

from ..models import HIVDisclosureStatusA, HIVDisclosureStatusB, HIVDisclosureStatusC
from ..models import HIVDisclosureStatusD
from .form_mixins import SubjectModelFormMixin

from flourish_form_validations.form_validators import HIVDisclosureStatusFormValidator


class HIVDisclosureStatusFormMixin(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = HIVDisclosureStatusFormValidator

    class Meta:
        abstract = True


class HIVDisclosureStatusFormA(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = HIVDisclosureStatusFormValidator

    class Meta:
        model = HIVDisclosureStatusA
        fields = '__all__'


class HIVDisclosureStatusFormB(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = HIVDisclosureStatusFormValidator

    class Meta:
        model = HIVDisclosureStatusB
        fields = '__all__'


class HIVDisclosureStatusFormC(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = HIVDisclosureStatusFormValidator

    class Meta:
        model = HIVDisclosureStatusC
        fields = '__all__'


class HIVDisclosureStatusFormD(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = HIVDisclosureStatusFormValidator

    class Meta:
        model = HIVDisclosureStatusD
        fields = '__all__'
