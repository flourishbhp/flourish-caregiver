from django import forms
from ..models import TbInterview
from .form_mixins import SubjectModelFormMixin


# from flourish_form_validations.form_validators import TbInterviewFormValidator
class TbInterviewForm(SubjectModelFormMixin, forms.ModelForm):

    # form_validator_cls = TbRoutineHealthScreenFormValidator

    class Meta:
        model = TbInterview
        fields = '__all__'
