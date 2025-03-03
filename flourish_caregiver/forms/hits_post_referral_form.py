from django import forms

from flourish_form_validations.form_validators import HITSPostReferralFormValidator

from .form_mixins import SubjectModelFormMixin
from ..models import HITSPostReferral


class HITSPostReferralForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = HITSPostReferralFormValidator

    class Meta:
        model = HITSPostReferral
        fields = '__all__'
