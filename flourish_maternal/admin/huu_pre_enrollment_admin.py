from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_maternal_admin
from ..forms import HuuPreEnrollmentForm
from ..models import HuuPreEnrollment


@admin.register(HuuPreEnrollment, site=flourish_maternal_admin)
class HuuPreEnrollmentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = HuuPreEnrollmentForm

    fieldsets = (
        (None, {
            'fields': [
                'report_datetime',
                'maternal_dob',
                'child_hiv_docs',
                'child_hiv_result',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'child_hiv_docs': admin.VERTICAL,
                    'child_hiv_result': admin.VERTICAL}

    search_fields = ['screening_identifier']
