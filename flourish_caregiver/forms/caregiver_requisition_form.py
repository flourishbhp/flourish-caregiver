from arrow.arrow import Arrow
from django import forms
from django.conf import settings
from django.utils import timezone
from edc_base.utils import convert_php_dateformat
from edc_form_validators import FormValidatorMixin
from edc_lab.forms.modelform_mixins import RequisitionFormMixin
from edc_senaite_interface.forms import SenaiteRequisitionFormValidatorMixin

from ..models import CaregiverRequisition
from .form_mixins import SubjectModelFormMixin


class CaregiverRequisitionForm(SubjectModelFormMixin, RequisitionFormMixin,
                               SenaiteRequisitionFormValidatorMixin,
                               FormValidatorMixin):

    requisition_identifier = forms.CharField(
        label='Requisition identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def clean(self):
        self.visit_obj = self.cleaned_data.get('maternal_visit')
        self.subject_identifier = self.cleaned_data.get(
            'maternal_visit').subject_identifier
        self.validate_estimated_volume()
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

    def validate_estimated_volume(self):
        # required fields
        panel = self.cleaned_data.get('panel')
        estimated_volume = self.cleaned_data.get('estimated_volume')

        if panel.name == 'breast_milk':
            if 4 > estimated_volume or estimated_volume > 20:
                raise forms.ValidationError({'estimated_volume': 'The estimated volume should be between 0 & 20 ml'})

    class Meta:
        model = CaregiverRequisition
        fields = '__all__'
