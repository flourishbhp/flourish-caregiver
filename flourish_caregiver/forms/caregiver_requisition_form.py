from arrow.arrow import Arrow
from django import forms
from django.conf import settings
from django.utils import timezone
from edc_base.utils import convert_php_dateformat
from edc_form_validators import FormValidatorMixin
from edc_lab.forms.modelform_mixins import RequisitionFormMixin

from ..models import CaregiverRequisition
from .form_mixins import SubjectModelFormMixin


class CaregiverRequisitionForm(SubjectModelFormMixin, RequisitionFormMixin,
                               FormValidatorMixin):

    requisition_identifier = forms.CharField(
        label='Requisition identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    
    def clean(self):
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        super().clean()

    def validate_requisition_datetime(self):
        requisition_datetime = self.cleaned_data.get('requisition_datetime')
        maternal_visit = self.cleaned_data.get('maternal_visit')
        if requisition_datetime:
            requisition_datetime = Arrow.fromdatetime(
                requisition_datetime, requisition_datetime.tzinfo).to('utc').datetime
            if requisition_datetime < maternal_visit.report_datetime:
                formatted = timezone.localtime(maternal_visit.report_datetime).strftime(
                    convert_php_dateformat(settings.SHORT_DATETIME_FORMAT))
                raise forms.ValidationError({
                    'requisition_datetime':
                    f'Invalid. Cannot be before date of visit {formatted}.'})

    class Meta:
        model = CaregiverRequisition
        fields = '__all__'
