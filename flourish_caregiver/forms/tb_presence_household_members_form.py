from django import forms

from flourish_form_validations.form_validators import TbPresenceHouseholdMembersFormValidator

from ..models import TbPresenceHouseholdMembers
from .form_mixins import SubjectModelFormMixin


class TbPresenceHouseholdMembersForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = TbPresenceHouseholdMembersFormValidator

    class Meta:
        model = TbPresenceHouseholdMembers
        fields = '__all__'
