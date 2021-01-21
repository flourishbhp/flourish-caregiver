from django import forms
from flourish_form_validations.form_validators import HIVRapidTestCounselingFormValidator

from ..models import HIVRapidTestCounseling
from .form_mixins import SubjectModelFormMixin


class HIVRapidTestCounselingForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = HIVRapidTestCounselingFormValidator

    class Meta:
        model = HIVRapidTestCounseling
        fields = '__all__'
