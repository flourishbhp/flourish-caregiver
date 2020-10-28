from django import forms
from ..models import MaternalUltraSoundInitial
from .form_mixins import SubjectModelFormMixin


class MaternalUltraSoundInitialForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = MaternalUltraSoundInitial
        fields = '__all__'
