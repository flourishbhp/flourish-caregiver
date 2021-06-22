from django.contrib import admin
from django.utils.safestring import mark_safe
from edc_appointment.admin import AppointmentAdmin as BaseAppointmentAdmin
from edc_appointment.admin_site import edc_appointment_admin
from edc_appointment.models import Appointment
from django.contrib.admin.sites import NotRegistered

try:
    edc_appointment_admin.unregister(Appointment)
except NotRegistered:
    pass


@admin.register(Appointment, site=edc_appointment_admin)
class AppointmentAdmin(BaseAppointmentAdmin):

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}
        app_obj = Appointment.objects.get(id=object_id)

        earliest_start = (app_obj.timepoint_opened_datetime -
                          app_obj.visits.get(app_obj.visit_code).rlower)

        latest_start = (app_obj.timepoint_opened_datetime +
                        app_obj.visits.get(app_obj.visit_code).rupper)

        extra_context.update({'earliest_start': earliest_start.strftime("%Y/%d/%m, %H:%M:%S"),
                              'latest_start': latest_start.strftime("%Y/%d/%m, %H:%M:%S"), })

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)

    def update_change_instructions(self, extra_context):
        extra_context = extra_context or {}
        extra_context[
            'instructions'] = self.change_instructions or self.instructions

        earliest_start = extra_context.get('earliest_start')
        latest_start = extra_context.get('latest_start')

        additional_instructions = mark_safe(
            f'<b>Earliest Start Date: {earliest_start} <Latest Start Date: {latest_start}</b> <BR>'
            'To start or continue to edit FORMS for this subject, change the '
            'appointment status below to "In Progress" and click SAVE. <BR>'
            '<i>Note: You may only edit one appointment at a time. '
            'Before you move to another appointment, change the appointment '
            'status below to "Incomplete or "Done".</i>')

        extra_context['additional_instructions'] = additional_instructions
        return extra_context
