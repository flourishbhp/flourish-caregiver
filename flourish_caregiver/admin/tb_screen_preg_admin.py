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
                'cough_lasted_2wks',
                'cough_blood_last_2wks',
                'have_fever',
                'fever_lasted_2wks',
                'have_night_sweats',
                'sweats_lasted_2wks',
                'have_enlarged_lymph',
                'unexplained_fatigue',
                'unexplained_weight_loss',
                'weight_gain_fail'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'have_cough': admin.VERTICAL,
                    'cough_lasted_2wks': admin.VERTICAL,
                    'cough_blood_last_2wks': admin.VERTICAL,
                    'have_fever': admin.VERTICAL,
                    'fever_lasted_2wks': admin.VERTICAL,
                    'have_night_sweats': admin.VERTICAL,
                    'sweats_lasted_2wks': admin.VERTICAL,
                    'have_enlarged_lymph': admin.VERTICAL,
                    'unexplained_fatigue': admin.VERTICAL,
                    'unexplained_weight_loss': admin.VERTICAL,
                    'weight_gain_fail': admin.VERTICAL}
