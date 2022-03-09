from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from flourish_caregiver.admin.modeladmin_mixins import CrfModelAdminMixin
from flourish_caregiver.admin_site import flourish_caregiver_admin
from flourish_caregiver.forms import TbVisitScreeningWomenForm
from flourish_caregiver.models import TbVisitScreeningWomen


@admin.register(TbVisitScreeningWomen, site=flourish_caregiver_admin)
class TbVisitScreeningWomenAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = TbVisitScreeningWomenForm

    fieldsets = (
        (None, {
            'fields': (
                'maternal_visit',
                'report_datetime',
                'have_cough',
                'cough_duration',
                'cough_intersects_preg',
                'cough_timing',
                'cough_intersects_preg_cough_duration',
                'fever',
                'fever_during_preg',
                'fever_timing',
                'night_sweats',
                'night_sweats_postpartum',
                'night_sweats_timing',
                'weight_loss',
                'weight_loss_postpartum',
                'weight_loss_timing',
                'cough_blood',
                'cough_blood_timing',
                'enlarged_lymph_nodes',
                'enlarged_lymph_nodes_postpartum',
                'lymph_nodes_timing',
                'unexplained_fatigue',
                'unexplained_fatigue_postpartum',
                'unexplained_fatigue_timing',
                'covid_19_test',
                'received_results',
                'covid_19_test_results',
                'tb_clinic_postpartum',

            )}
         ),
        audit_fieldset_tuple
    )

    radio_fields = {
        'have_cough': admin.VERTICAL,
        'cough_duration': admin.VERTICAL,
        'cough_intersects_preg': admin.VERTICAL,
        'cough_timing': admin.VERTICAL,
        'cough_intersects_preg_cough_duration': admin.VERTICAL,
        'fever': admin.VERTICAL,
        'fever_during_preg': admin.VERTICAL,
        'fever_timing': admin.VERTICAL,
        'night_sweats': admin.VERTICAL,
        'night_sweats_postpartum': admin.VERTICAL,
        'night_sweats_timing': admin.VERTICAL,
        'weight_loss': admin.VERTICAL,
        'weight_loss_postpartum': admin.VERTICAL,
        'weight_loss_timing': admin.VERTICAL,
        'cough_blood': admin.VERTICAL,
        'cough_blood_timing': admin.VERTICAL,
        'enlarged_lymph_nodes': admin.VERTICAL,
        'enlarged_lymph_nodes_postpartum': admin.VERTICAL,
        'lymph_nodes_timing': admin.VERTICAL,
        'unexplained_fatigue': admin.VERTICAL,
        'unexplained_fatigue_postpartum': admin.VERTICAL,
        'unexplained_fatigue_timing': admin.VERTICAL,
        'covid_19_test': admin.VERTICAL,
        'received_results': admin.VERTICAL,
        'covid_19_test_results': admin.VERTICAL,
        'tb_clinic_postpartum': admin.VERTICAL,
    }
