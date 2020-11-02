from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_caregiver_admin
from ..forms import LocatorLogForm, LocatorLogEntryForm
from ..models import LocatorLog, LocatorLogEntry
from .modeladmin_mixins import ModelAdminMixin


@admin.register(LocatorLog, site=flourish_caregiver_admin)
class LocatorLogAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = LocatorLogForm

    fieldsets = (
        (None, {
            'fields': [
                'study_maternal_identifier',
                'report_datetime',
            ]}
         ), audit_fieldset_tuple)


@admin.register(LocatorLogEntry, site=flourish_caregiver_admin)
class LocatorLogEntryAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = LocatorLogEntryForm

    fieldsets = (
        (None, {
            'fields': [
                'locator_log',
                'report_datetime',
                'report_date',
                'log_status',
                'comment',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'log_status': admin.VERTICAL}
