from django import forms
from ..models import UltraSound
from .form_mixins import SubjectModelFormMixin


class UltraSoundForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = UltraSound
        fields = '__all__'
