from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_maternal_admin
from ..forms import MaternalEnrollmentForm
from ..models import MaternalEnrollment


@admin.register(MaternalEnrollment, site=flourish_maternal_admin)
class MaternalEnrollmentAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = MaternalEnrollmentForm

    fieldsets = (
        (None, {
            'fields': [
                'report_datetime',
                'maternal_prev_enroll',
                'current_hiv_status',
                'last_test_date',
                'test_date',
                'is_date_estimated',
                'dob',
                'sex',
                'relation_to_child',
                'relation_to_child_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'maternal_prev_enroll': admin.VERTICAL,
                    'current_hiv_status': admin.VERTICAL,
                    'last_test_date': admin.VERTICAL,
                    'is_date_estimated': admin.VERTICAL,
                    'relation_to_child': admin.VERTICAL}

    search_fields = ['screening_identifier']
