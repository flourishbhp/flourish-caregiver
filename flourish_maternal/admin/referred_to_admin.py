from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_maternal_admin
from ..forms import ReferredToForm
from ..models import ReferredTo


@admin.register(ReferredTo, site=flourish_maternal_admin)
class ReferredToAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ReferredToForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'referred_to',
                'referred_to_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'referred_to': admin.VERTICAL}
