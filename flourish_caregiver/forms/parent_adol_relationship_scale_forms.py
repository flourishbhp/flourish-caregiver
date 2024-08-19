from django import forms

from .form_mixins import InlineSubjectModelFormMixin, SubjectModelFormMixin
from ..models import ParentAdolRelationshipScale, ParentAdolReloScaleParentModel


class ParentAdolRelationshipScaleForm(InlineSubjectModelFormMixin):
    associated_child_identifier = forms.CharField(
        label='Associated child identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = ParentAdolRelationshipScale
        fields = '__all__'


class ParentAdolRelationshipScaleParentForm(SubjectModelFormMixin, forms.ModelForm):
    class Meta:
        model = ParentAdolReloScaleParentModel
        fields = '__all__'
