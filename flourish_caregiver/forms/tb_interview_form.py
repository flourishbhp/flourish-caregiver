from django import forms

from flourish_form_validations.form_validators import TbInterviewFormValidator

from ..models import TbInterview
from .form_mixins import SubjectModelFormMixin


class TbInterviewForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = TbInterviewFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['translator_name'].widget = forms.RadioSelect(
            choices=self.instance.ra_users)

        self.fields['transcriber_name'].widget = forms.RadioSelect(
            choices=self.instance.ra_users)

    class Meta:
        model = TbInterview
        fields = '__all__'
