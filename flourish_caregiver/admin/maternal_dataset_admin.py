from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalDatasetForm
from ..models import MaternalDataset
from .modeladmin_mixins import ModelAdminMixin


@admin.register(MaternalDataset, site=flourish_caregiver_admin)
class MaternalDatasetAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = MaternalDatasetForm

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'screening_identifier',
                'study_child_identifier',
                'study_maternal_identifier',
                'mom_enrolldate',
                'protocol',
                'delivdt',
                'site_name',
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
                'twin_triplet',
                'preg_dtg',
                'preg_pi',
                'preg_efv',
            ]}
         ), audit_fieldset_tuple)

    search_fields = ['subject_identifier', 'study_maternal_identifier', 'screening_identifier']
