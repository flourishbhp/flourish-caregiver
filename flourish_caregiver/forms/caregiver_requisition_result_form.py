from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import CaregiverRequisitionResult


class CaregiverRequisitionResultForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = CaregiverRequisitionResult
        fields = '__all__'
