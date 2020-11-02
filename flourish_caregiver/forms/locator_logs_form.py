from django import forms

from edc_base.sites import SiteModelFormMixin

from ..models import LocatorLog, LocatorLogEntry


class LocatorLogForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = LocatorLog
        fields = '__all__'


class LocatorLogEntryForm(forms.ModelForm):

    report_date = forms.CharField(
        label='Report Date',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = LocatorLogEntry
        fields = '__all__'
