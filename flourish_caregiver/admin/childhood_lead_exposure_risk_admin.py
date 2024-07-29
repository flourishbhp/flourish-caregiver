from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from flourish_caregiver.admin.modeladmin_mixins import CrfModelAdminMixin
from flourish_caregiver.admin_site import flourish_caregiver_admin
from flourish_caregiver.forms import ChildhoodLeadExposureRiskForm
from flourish_caregiver.models import ChildhoodLeadExposureRisk


@admin.register(ChildhoodLeadExposureRisk,  site=flourish_caregiver_admin)
class ChildhoodLeadExposureRiskAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = ChildhoodLeadExposureRiskForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'residence_age',
                'lead_exposure_test',
                'suck_fingers',
                'eats_soil',
                'eats_paint_chips',
                'eating_keys',
                'eating_jewellery',
                'relative_paints',
                'home_business',
                'home_run_business',
                'home_run_business_other',
                'relative_work_batteries',
                'relative_repairs_cars',
                'unusable_vehicles',
                'traditional_remedies',
                'peeling_paint',
                'house_by_busy_road',
                'years_near_busy_road',
                'pr_male_caregiver_edu',
                'child_restless',
                'house_year_built',
            ]
        }), audit_fieldset_tuple)

    radio_fields = {
        'lead_exposure_test': admin.VERTICAL,
        'suck_fingers': admin.VERTICAL,
        'eats_soil': admin.VERTICAL,
        'eats_paint_chips': admin.VERTICAL,
        'eating_keys': admin.VERTICAL,
        'eating_jewellery': admin.VERTICAL,
        'relative_paints': admin.VERTICAL,
        'home_business': admin.VERTICAL,
        'home_run_business': admin.VERTICAL,
        'relative_work_batteries': admin.VERTICAL,
        'relative_repairs_cars': admin.VERTICAL,
        'unusable_vehicles': admin.VERTICAL,
        'traditional_remedies': admin.VERTICAL,
        'peeling_paint': admin.VERTICAL,
        'house_by_busy_road': admin.VERTICAL,
        'pr_male_caregiver_edu': admin.VERTICAL,
        'child_restless': admin.VERTICAL,
        'house_year_built': admin.VERTICAL,
    }
