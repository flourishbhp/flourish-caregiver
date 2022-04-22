from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import FlourishConsentVersionForm
from ..models import FlourishConsentVersion
from .modeladmin_mixins import ModelAdminMixin


@admin.register(FlourishConsentVersion, site=flourish_caregiver_admin)
class FlourishConsentVersionAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = FlourishConsentVersionForm

    fieldsets = (
        (None, {
            'fields': [
                'screening_identifier',
                'report_datetime',
                'version']}
         ), audit_fieldset_tuple)

    radio_fields = {'version': admin.VERTICAL}

    list_display = ('screening_identifier',
                    'report_datetime',
                    'version',)
