from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin, ModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalArvPostAdherenceForm
from ..models import MaternalArvPostAdherence


@admin.register(MaternalArvPostAdherence, site=flourish_caregiver_admin)
class MaternalArvPostAdherenceAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = MaternalArvPostAdherenceForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'missed_arv',
                'interruption_reason',
                'interruption_reason_other',
                'comment']}
         ), audit_fieldset_tuple)

    radio_fields = {'interruption_reason': admin.VERTICAL}
