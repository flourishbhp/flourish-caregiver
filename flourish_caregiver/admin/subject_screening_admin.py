from django.contrib import admin

from ..admin_site import flourish_caregiver_admin
from ..forms import SubjectScreeningForm
from ..models import SubjectScreening
from .modeladmin_mixins import ModelAdminMixin


@admin.register(SubjectScreening, site=flourish_caregiver_admin)
class SubjectScreeningAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = SubjectScreeningForm
    search_fields = ['subject_identifier']

    fields = ('screening_identifier',
              'report_datetime',
              'age_in_years',
              'has_omang',
              'has_child')

    radio_fields = {'has_omang': admin.VERTICAL,
                    'has_child': admin.VERTICAL,}

    list_display = (
        'report_datetime', 'age_in_years', 'has_child', 'is_eligible', 'is_consented')

    list_filter = ('report_datetime', 'is_eligible', 'has_child', 'is_consented')
