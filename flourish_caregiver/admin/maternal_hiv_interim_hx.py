from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalHivInterimHxForm
from ..models import MaternalHivInterimHx
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(MaternalHivInterimHx, site=flourish_caregiver_admin)
class MaternalHivInterimHxAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MaternalHivInterimHxForm
    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'has_cd4',
                'cd4_date',
                'cd4_result',
                'has_vl',
                'vl_date',
                'vl_detectable',
                'vl_result',
                'comment']}
         ), audit_fieldset_tuple)

    radio_fields = {'has_cd4': admin.VERTICAL,
                    'has_vl': admin.VERTICAL,
                    'vl_detectable': admin.VERTICAL}

    list_display = ('maternal_visit', 'report_datetime', 'has_cd4', 'has_vl')
