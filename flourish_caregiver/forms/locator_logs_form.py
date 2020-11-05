from django import forms

from edc_base.sites import SiteModelFormMixin

from ..models import LocatorLog, LocatorLogEntry


class LocatorLogForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = LocatorLog
        fields = '__all__'


class LocatorLogEntryForm(forms.ModelForm):

    class Meta:
        model = LocatorLogEntry
        fields = '__all__'
