from django import forms
from flourish_form_validations.form_validators import TbEngagementFormValidator

from ..models import TbEngagement
from .form_mixins import SubjectModelFormMixin


class TbEngagementForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = TbEngagementFormValidator

    class Meta:
        model = TbEngagement
        fields = '__all__'
