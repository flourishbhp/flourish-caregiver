from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import CyhuuPreEnrollmentForm
from ..models import CyhuuPreEnrollment


@admin.register(CyhuuPreEnrollment, site=flourish_caregiver_admin)
class CyhuuPreEnrollmentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CyhuuPreEnrollmentForm

    fieldsets = (
        (None, {
            'fields': [
                'report_datetime',
                'biological_mother',
                'child_dob',
                'hiv_docs',
                'hiv_test_result',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'biological_mother': admin.VERTICAL,
                    'hiv_docs': admin.VERTICAL,
                    'hiv_test_result': admin.VERTICAL}

    search_fields = ['screening_identifier']
