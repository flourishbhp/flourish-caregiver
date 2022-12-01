from django import forms
from ..models import TbInterviewTranslation
from .form_mixins import SubjectModelFormMixin


class TbInterviewTranslationForm(SubjectModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['translator_name'].widget = forms.RadioSelect(
            choices=self.instance.intv_users)

    class Meta:
        model = TbInterviewTranslation
        fields = '__all__'
