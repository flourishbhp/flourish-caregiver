from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import InterviewFocusGroupInterest


class InterviewFocusGroupInterestForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = InterviewFocusGroupInterest
        fields = '__all__'

