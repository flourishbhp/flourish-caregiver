from django import forms

from ..models import TbEngagement
from .form_mixins import SubjectModelFormMixin


class TbEngagementForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = TbEngagement
        fields = '__all__'
