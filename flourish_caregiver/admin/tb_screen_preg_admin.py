from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import TbScreenPregForm
from ..models import TbScreenPreg


@admin.register(TbScreenPreg, site=flourish_caregiver_admin)
class TbScreenPregAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = TbScreenPregForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'have_cough',
                'have_fever',
                'night_sweats',
                'weight_loss',
                'cough_blood',
                'enlarged_lymph',
                'unexplained_fatigue',
                'tb_screened',
                'where_screened',
                'where_screened_other',
                'tb_symptom_screened',
                'diagnostic_evaluation'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'have_cough': admin.VERTICAL,
                    'have_fever': admin.VERTICAL,
                    'night_sweats': admin.VERTICAL,
                    'weight_loss': admin.VERTICAL,
                    'cough_blood': admin.VERTICAL,
                    'enlarged_lymph': admin.VERTICAL,
                    'unexplained_fatigue': admin.VERTICAL,
                    'tb_screened': admin.VERTICAL,
                    'where_screened': admin.VERTICAL,
                    'tb_symptom_screened': admin.VERTICAL,
                    'diagnostic_evaluation': admin.VERTICAL}
