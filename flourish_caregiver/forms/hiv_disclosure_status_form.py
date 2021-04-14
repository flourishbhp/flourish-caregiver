from django import forms

from ..models import HIVDisclosureStatus
from .form_mixins import SubjectModelFormMixin


class HIVDisclosureStatusForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = HIVDisclosureStatus
        fields = '__all__'
