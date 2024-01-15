from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import HITSScreening


class HITSScreeningForm(SubjectModelFormMixin, forms.ModelForm):
    score = forms.CharField(
        label='Total HITS Score',
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = HITSScreening
        fields = '__all__'
