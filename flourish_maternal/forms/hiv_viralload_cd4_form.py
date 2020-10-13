from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import HivViralLoadAndCd4


class HivViralLoadCd4Form(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = HivViralLoadAndCd4
        fields = '__all__'
