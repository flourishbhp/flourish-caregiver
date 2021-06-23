from django import forms

from ..models import ClinicianNotes, ClinicianNotesImage
from .form_mixins import SubjectModelFormMixin, InlineSubjectModelFormMixin


class ClinicianNotesForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = ClinicianNotes
        fields = '__all__'


class ClinicianNotesImageForm(InlineSubjectModelFormMixin):

    class Meta:
        model = ClinicianNotesImage
        fields = '__all__'
