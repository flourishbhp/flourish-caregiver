from django import forms
from edc_base.sites.forms import SiteModelFormMixin

from ..models import MaternalDataset


class MaternalDatasetForm(SiteModelFormMixin, forms.ModelForm):

    class Meta:
        model = MaternalDataset
        fields = '__all__'
