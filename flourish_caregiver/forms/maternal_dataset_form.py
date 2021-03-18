from django import forms
from edc_base.sites.forms import SiteModelFormMixin

from ..models import MaternalDataset


class MaternalDatasetForm(SiteModelFormMixin, forms.ModelForm):

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    screening_identifier = forms.CharField(
        label='Eligibility Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    study_maternal_identifier = forms.CharField(
        label='Study maternal Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_enrolldate = forms.CharField(
        label='Maternal enrollment date',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    protocol = forms.CharField(
        label='Protocol',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    delivdt = forms.CharField(
        label='Delivery date',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    site_name = forms.CharField(
        label='Maternal enrollment date',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    delivmeth = forms.CharField(
        label='Method of delivery',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    delivery_location = forms.CharField(
        label='Delivery location',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    ega_delivery = forms.CharField(
        label='EGA at delivery',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_age_enrollment = forms.CharField(
        label='Mother\'s age at enrollment',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_hivstatus = forms.CharField(
        label='Maternal HIV infection status',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    parity = forms.CharField(
        label='Parity',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    gravida = forms.CharField(
        label='Gravida',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_education = forms.CharField(
        label='Maternal education level',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_maritalstatus = forms.CharField(
        label='Maternal marital status',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_personal_earnings = forms.CharField(
        label='Mother\'s personal earnings',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_moneysource = forms.CharField(
        label='Maternal source of income',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_occupation = forms.CharField(
        label='Mother\'s occupation',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_pregarv_strat = forms.CharField(
        label='Maternal ARVs during pregnancy',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_arvstart_date = forms.CharField(
        label='Date mother started HAART',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_baseline_cd4 = forms.CharField(
        label='Maternal baseline CD4 count',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_baseline_cd4date = forms.CharField(
        label='Draw data of mother\'s baseline CD4',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_baseline_vl = forms.CharField(
        label='Maternal baseline viral load',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_baseline_vldate = forms.CharField(
        label='Draw date of mother\'s baseline VL',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_baseline_hgb = forms.CharField(
        label='Maternal baseline HGB',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_baseline_hgbdt = forms.CharField(
        label='Date of maternal baseline HGB',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    mom_deathdate = forms.CharField(
        label='Date mother died',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = MaternalDataset
        fields = '__all__'
