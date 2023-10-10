import datetime
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import get_utcnow
from edc_fieldsets.fieldlist import Insert
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalArvPostAdherenceForm
from ..models import MaternalArvPostAdherence


@admin.register(MaternalArvPostAdherence, site=flourish_caregiver_admin)
class MaternalArvPostAdherenceAdmin(CrfModelAdminMixin, admin.ModelAdmin):
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

    radio_fields = {'stopped_art_past_yr': admin.VERTICAL}

    filter_horizontal = ('interruption_reason', 'stopped_art_reasons', )

    conditional_fieldlists = {
        'version_2': Insert(
            'stopped_art_past_yr',
            'stopped_art_freq',
            'stopped_art_reasons',
            'stopped_reasons_other',
            after='interruption_reason_other')}

    def get_key(self, request, obj=None):
        try:
            model_obj = self.get_instance(request)
        except ObjectDoesNotExist:
            return None
        else:
            maternal_visit = getattr(model_obj, 'maternalvisit', None)
            report_date = getattr(maternal_visit, 'report_datetime', get_utcnow()).date()
            version2_date = datetime.date(2023, 10, 6)
            if report_date >= version2_date:
                return 'version_2'
