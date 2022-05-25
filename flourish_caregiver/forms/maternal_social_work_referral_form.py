from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import MaternalSocialWorkReferral


class MaternalSocialWorkReferralForm(SubjectModelFormMixin, forms.ModelForm):

    # form_validator_cls = None

    class Meta:
        model = MaternalSocialWorkReferral
        fields = '__all__'
