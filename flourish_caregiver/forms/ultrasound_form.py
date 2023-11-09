from django import forms

from flourish_form_validations.form_validators import UltrasoundFormValidator
from .form_mixins import SubjectModelFormMixin
from ..helper_classes.utils import get_child_subject_identifier_by_visit
from ..models import UltraSound


class UltraSoundForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = UltrasoundFormValidator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.fields['maternal_visit']._queryset.exists():
            child_subject_identifier = get_child_subject_identifier_by_visit(
                self.fields['maternal_visit']._queryset[0])
            self.fields['child_subject_identifier'].initial = child_subject_identifier
            self.fields['child_subject_identifier'].widget.attrs['readonly'] = True

    class Meta:
        model = UltraSound
        fields = '__all__'
