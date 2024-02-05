import datetime
import pandas as pd

from io import BytesIO
from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from edc_lab.admin import RequisitionAdminMixin
from edc_lab.admin import requisition_verify_fields
from edc_lab.admin import requisition_verify_fieldset, requisition_status_fieldset
from edc_model_admin import audit_fieldset_tuple

from edc_senaite_interface.admin import SenaiteRequisitionAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverRequisitionForm
from ..models import CaregiverRequisition
from .modeladmin_mixins import CrfModelAdminMixin

requisition_identifier_fields = (
    'requisition_identifier',
    'identifier_prefix',
    'primary_aliquot_identifier',
)

requisition_identifier_fieldset = (
    'Identifiers', {
        'classes': ('collapse',),
        'fields': (requisition_identifier_fields)})


class ExportRequisitionCsvMixin:

    def fix_date_format(self, obj_dict=None):
        """Change all dates into a format for the export
        and split the time into a separate value.

        Format: m/d/y
        """

        result_dict_obj = {**obj_dict}
        for key, value in obj_dict.items():
            if isinstance(value, datetime.datetime):
                value = timezone.make_naive(value)
                time_value = value.time()
                time_variable = key + '_time'
                result_dict_obj[key] = value.date()
                result_dict_obj[time_variable] = time_value
        return result_dict_obj

    def export_as_csv(self, request, queryset):
        records = []
        for obj in queryset:
            obj_data = self.fix_date_format(obj.__dict__)
            # data = [obj_data.get(field, '') for field in field_names]
            obj_data.update(panel_name=obj.panel.name)
            records.append(obj_data)

        excel_buffer = BytesIO()
        writer = pd.ExcelWriter(excel_buffer, engine='openpyxl')

        df = pd.DataFrame(records)
        df.to_excel(writer, sheet_name=f'{self.model.__name__}', index=False)

        # Close the workbook
        writer.close()

        excel_buffer.seek(0)

        workbook = excel_buffer.read()

        # Create an HTTP response with the Excel file as an attachment
        response = HttpResponse(
            workbook,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        response['Content-Disposition'] = f'attachment; filename={self.get_export_filename()}.xlsx'

        return response

    export_as_csv.short_description = 'Export with panel name'


@admin.register(CaregiverRequisition, site=flourish_caregiver_admin)
class CaregiverRequisitionAdmin(ExportRequisitionCsvMixin, CrfModelAdminMixin,
                                RequisitionAdminMixin,
                                SenaiteRequisitionAdminMixin,
                                admin.ModelAdmin):

    form = CaregiverRequisitionForm
    actions = ['export_as_csv']
    ordering = ('requisition_identifier',)

    fieldsets = (
        (None, {
            'fields': (
                'maternal_visit',
                'requisition_datetime',
                'is_drawn',
                'reason_not_drawn',
                'reason_not_drawn_other',
                'drawn_datetime',
                'study_site',
                'panel',
                'item_type',
                'item_count',
                'estimated_volume',
                'priority',
                'exists_on_lis',
                'sample_id',
                'comments',
            )}),
        requisition_status_fieldset,
        requisition_identifier_fieldset,
        requisition_verify_fieldset,
        audit_fieldset_tuple)

    radio_fields = {
        'is_drawn': admin.VERTICAL,
        'reason_not_drawn': admin.VERTICAL,
        'item_type': admin.VERTICAL,
        'priority': admin.VERTICAL,
        'study_site': admin.VERTICAL,
        'exists_on_lis': admin.VERTICAL,
    }

    list_display = ('maternal_visit', 'is_drawn', 'panel', 'estimated_volume',)

    def get_readonly_fields(self, request, obj=None):
        on_lis = getattr(obj, 'sample_id', None)
        read_only = (super().get_readonly_fields(request, obj)
                     + requisition_identifier_fields
                     + requisition_verify_fields)
        return read_only + ('exists_on_lis', 'sample_id', ) if on_lis else read_only

    def get_previous_instance(self, request, instance=None, **kwargs):
        """Returns a model instance that is the first occurrence of a previous
        instance relative to this object's appointment.
        """
        obj = None
        appointment = instance or self.get_instance(request)

        if appointment:
            while appointment:
                options = {
                    '{}__appointment'.format(self.model.visit_model_attr()):
                        self.get_previous_appt_instance(appointment)
                }
                obj = self.model.objects.filter(**options).first()
                appointment = self.get_previous_appt_instance(appointment)
        return obj
