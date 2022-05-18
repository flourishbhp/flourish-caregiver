from django import forms

from flourish_caregiver.forms.form_mixins import SubjectModelFormMixin
from flourish_caregiver.models import TbReferral


class TbReferralForm(SubjectModelFormMixin, forms.ModelForm):
    class Meta:
        model = TbReferral
        fields = '__all__'
