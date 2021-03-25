from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverPreviouslyEnrolledForm
from ..models import CaregiverPreviouslyEnrolled


@admin.register(CaregiverPreviouslyEnrolled, site=flourish_caregiver_admin)
class CaregiverPreviouslyEnrolledAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CaregiverPreviouslyEnrolledForm

    fieldsets = (
        (None, {
            'fields': [
                'report_datetime',
                'subject_identifier',
                'maternal_prev_enroll',
                'current_hiv_status',
                'last_test_date',
                'test_date',
                'is_date_estimated',
                'sex',
                'relation_to_child',
                'relation_to_child_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'maternal_prev_enroll': admin.VERTICAL,
                    'current_hiv_status': admin.VERTICAL,
                    'last_test_date': admin.VERTICAL,
                    'is_date_estimated': admin.VERTICAL,
                    'sex': admin.VERTICAL,
                    'relation_to_child': admin.VERTICAL}

    search_fields = ['subject_identifier']
