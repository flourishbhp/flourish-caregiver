from django import forms

from flourish_form_validations.form_validators import TbReferralOutcomesFormValidator

from ..models import TbReferralOutcomes
from .form_mixins import SubjectModelFormMixin


class TbReferralOutcomesForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = TbReferralOutcomesFormValidator

    class Meta:
        model = TbReferralOutcomes
        fields = '__all__'
