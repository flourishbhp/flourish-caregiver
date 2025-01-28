from django.contrib import admin
from edc_model_admin import TabularInlineMixin
from edc_odk.admin import ODKActionMixin

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import ClinicianNotesForm, ClinicianNotesImageForm
from ..models import ClinicianNotes, ClinicianNotesImage


class ClinicianNotesImageInline(TabularInlineMixin, admin.TabularInline):

    model = ClinicianNotesImage
    form = ClinicianNotesImageForm
    extra = 0

    fields = ('clinician_notes_image', 'image', 'user_uploaded',
              'datetime_captured', 'modified', 'hostname_created',)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        fields = ('clinician_notes_image', 'datetime_captured',
                  'user_uploaded') + fields

        return fields


@admin.register(ClinicianNotes, site=flourish_caregiver_admin)
class ClinicianNotesAdmin(ODKActionMixin, CrfModelAdminMixin, admin.ModelAdmin):
    form = ClinicianNotesForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
            ]}
         ),)

    inlines = [ClinicianNotesImageInline]
