from django import forms
from ..models import TbInterviewTranscription
from .form_mixins import SubjectModelFormMixin


class TbInterviewTranscriptionForm(SubjectModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['transcriber_name'].widget = forms.RadioSelect(
            choices=self.instance.intv_users)

    class Meta:
        model = TbInterviewTranscription
        fields = '__all__'
