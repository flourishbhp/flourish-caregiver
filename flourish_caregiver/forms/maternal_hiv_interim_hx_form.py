from django import forms
from .form_mixins import SubjectModelFormMixin
from ..models import MaternalHivInterimHx


class MaternalHivInterimHxForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = MaternalHivInterimHx
        fields = '__all__'
