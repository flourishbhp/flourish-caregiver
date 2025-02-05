from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_fieldsets.fieldlist import Insert
from edc_model_admin.model_admin_audit_fields_mixin import audit_fieldset_tuple

from flourish_child.admin import PreviousResultsAdminMixin
from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverTBScreeningForm
from ..models import CaregiverTBScreening


@admin.register(CaregiverTBScreening, site=flourish_caregiver_admin)
class CaregiverTBScreeningAdmin(CrfModelAdminMixin, PreviousResultsAdminMixin,
                                admin.ModelAdmin):
    form = CaregiverTBScreeningForm

    visit_attr = 'maternal_visit'

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'cough',
                'cough_duration',
                'fever',
                'fever_duration',
                'sweats',
                'sweats_duration',
                'weight_loss',
                'weight_loss_duration',
                'household_diagnosed_with_tb',
                'evaluated_for_tb',
                'flourish_referral',
                'clinic_visit_date',
                'tb_tests',
                'other_test',
                'chest_xray_results',
                'sputum_sample_results',
                'stool_sample_results',
                'urine_test_results',
                'skin_test_results',
                'blood_test_results',
                'other_test_results',
                'diagnosed_with_TB',
                'diagnosed_with_TB_other',
                'started_on_TB_treatment',
                'started_on_TB_treatment_other',
                'started_on_TB_preventative_therapy',
                'started_on_TB_preventative_therapy_other',
            ]}),
        audit_fieldset_tuple
    )

    radio_fields = {
        'cough': admin.VERTICAL,
        'cough_duration': admin.VERTICAL,
        'fever': admin.VERTICAL,
        'fever_duration': admin.VERTICAL,
        'sweats': admin.VERTICAL,
        'sweats_duration': admin.VERTICAL,
        'weight_loss': admin.VERTICAL,
        'weight_loss_duration': admin.VERTICAL,
        'household_diagnosed_with_tb': admin.VERTICAL,
        'evaluated_for_tb': admin.VERTICAL,
        'flourish_referral': admin.VERTICAL,
        'chest_xray_results': admin.VERTICAL,
        'sputum_sample_results': admin.VERTICAL,
        'stool_sample_results': admin.VERTICAL,
        'urine_test_results': admin.VERTICAL,
        'skin_test_results': admin.VERTICAL,
        'blood_test_results': admin.VERTICAL,
        'diagnosed_with_TB': admin.VERTICAL,
        'started_on_TB_treatment': admin.VERTICAL,
        'started_on_TB_preventative_therapy': admin.VERTICAL,
    }

    filter_horizontal = ('tb_tests',)

    update_fields = [
        'chest_xray_results',
        'sputum_sample_results',
        'stool_sample_results',
        'urine_test_results',
        'skin_test_results',
        'blood_test_results',
    ]

    def get_key(self, request, obj=None):
        try:
            model_obj = self.get_instance(request)
        except ObjectDoesNotExist:
            return None
        else:
            return getattr(model_obj, 'schedule_name', None)

    @property
    def quarterly_schedules(self):
        schedules = self.cohort_schedules_cls.objects.filter(
            schedule_type__icontains='quarterly',
            onschedule_model__startswith='flourish_caregiver').values_list(
                'schedule_name', flat=True)
        return schedules
