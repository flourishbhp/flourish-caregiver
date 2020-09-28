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
                'subject_identifier',
                'infant_identifier',
                'protocol',
                'site_name',
                'enrollment_date',
                'delivery_method',
                'delivery_location',
                'enrollment_age',
                'hiv_status',
                'parity',
                'gravida',
                'educational_level',
                'marital_status',
                'personal_earnings',
                'source_of_income',
                'occupation',
                'pregarv_strat',
                'arvstart_date',
                'baseline_cd4',
                'baseline_cd4date',
                'baseline_vl',
                'baseline_vldate',
                'baseline_hgb',
                'baseline_hgbdt',
                'death_date',
            ]}
         ), audit_fieldset_tuple)

    search_fields = ['subject_identifier']
