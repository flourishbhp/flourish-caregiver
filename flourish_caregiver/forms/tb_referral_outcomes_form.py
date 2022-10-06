from django import forms
from ..models import TbReferralOutcomes
from .form_mixins import SubjectModelFormMixin


class TbReferralOutcomesForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = TbReferralOutcomes
        fields = '__all__'
