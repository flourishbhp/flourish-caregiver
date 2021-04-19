from django import forms

from ..models import HIVDisclosureStatus
from .form_mixins import SubjectModelFormMixin

from flourish_form_validations.form_validators import HIVDisclosureStatusFormValidator


class HIVDisclosureStatusForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = HIVDisclosureStatusFormValidator

    class Meta:
        model = HIVDisclosureStatus
        fields = '__all__'
