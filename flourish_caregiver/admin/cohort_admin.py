from django.contrib import admin

from ..admin_site import flourish_caregiver_admin
from ..forms import CohortForm
from ..models import Cohort
from .modeladmin_mixins import ModelAdminMixin


@admin.register(Cohort, site=flourish_caregiver_admin)
class CohortAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = CohortForm
    search_fields = ['subject_identifier']

    fields = ('name',
              'assign_datetime',
              'enrollment_cohort', )

    list_display = ('subject_identifier', 'assign_datetime', 'enrollment_cohort', )
