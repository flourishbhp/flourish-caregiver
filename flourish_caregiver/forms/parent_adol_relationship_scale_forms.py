from django import forms
from .form_mixins import SubjectModelFormMixin
from ..models import ParentAdolRelationshipScale


class ParentAdolRelationshipScaleForm(SubjectModelFormMixin, forms.ModelForm):
    class Meta:
        model = ParentAdolRelationshipScale
        fields = '__all__'
