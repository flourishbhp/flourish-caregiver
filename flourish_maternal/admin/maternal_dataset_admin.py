from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from edc_base.sites.admin import ModelAdminSiteMixin
from ..admin_site import flourish_maternal_admin
from ..forms import MaternalDatasetForm
from ..models import MaternalDataset


@admin.register(MaternalDataset, site=flourish_maternal_admin)
class MaternalDatasetAdmin(ModelAdminSiteMixin, admin.ModelAdmin):

    form = MaternalDatasetForm

    fieldsets = (
        (None, {
            'fields': [
                'bid',
                'm_bid',
                'protocol',
                'delivdt',
                'site_name',
                'mom_enrolldate',
                'delivmeth',
                'delivery_location',
                'ega_delivery',
                'mom_age_enrollment',
                'mom_hivstatus',
                'parity',
                'gravida',
                'mom_education',
                'mom_maritalstatus',
                'mom_personal_earnings',
                'mom_moneysource',
                'mom_occupation',
                'mom_pregarv_strat',
                'mom_arvstart_date',
                'mom_baseline_cd4',
                'mom_baseline_cd4date',
                'mom_baseline_vl',
                'mom_baseline_vldate',
                'mom_baseline_hgb',
                'mom_baseline_hgbdt',
                'mom_deathdate',
            ]}
         ), audit_fieldset_tuple)

    search_fields = ['subject_identifier']
