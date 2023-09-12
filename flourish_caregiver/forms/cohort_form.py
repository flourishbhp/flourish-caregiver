from django import forms
from edc_base.sites import SiteModelFormMixin

from ..models import Cohort


class CohortForm(SiteModelFormMixin,
                 forms.ModelForm):

    class Meta:
        model = Cohort
        fields = '__all__'
