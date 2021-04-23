from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalDeliveryForm
from ..models import MaternalDelivery
from .modeladmin_mixins import ModelAdminMixin


@admin.register(MaternalDelivery, site=flourish_caregiver_admin)
class MaternalDeliveryAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = MaternalDeliveryForm

    list_display = ('subject_identifier',
                    'delivery_datetime',
                    'labour_hrs',
                    'delivery_hospital',
                    'valid_regiment_duration')

    list_filter = ('delivery_hospital',
                   'valid_regiment_duration')

    fieldsets = (
        (None, {
            'fields': [
                'subject_identifier',
                'report_datetime',
                'delivery_datetime',
                'delivery_time_estimated',
                'delivery_hospital',
                'delivery_hospital_other',
                'labour_hrs',
                'mode_delivery',
                'mode_delivery_other',
                'csection_reason',
                'csection_reason_other',
                'delivery_complications',
                'delivery_complications_other',
                'live_infants_to_register',
                'still_births',
                'valid_regiment_duration',
                'arv_initiation_date',
                'delivery_comment',
                'comment',
                'feeding_mode']}
         ), audit_fieldset_tuple)

    search_fields = ('subject_identifier',)

    radio_fields = {'delivery_time_estimated': admin.VERTICAL,
                    'delivery_hospital': admin.VERTICAL,
                    'valid_regiment_duration': admin.VERTICAL,
                    'mode_delivery': admin.VERTICAL,
                    'csection_reason': admin.VERTICAL,
                    'feeding_mode': admin.VERTICAL}

    filter_horizontal = ('delivery_complications',)
