from django import forms
from ..models import MaternalInterimIdcc
from .form_mixins import SubjectModelFormMixin


class MaternalInterimIdccForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = None

    class Meta:
        model = MaternalInterimIdcc
        fields = '__all__'
