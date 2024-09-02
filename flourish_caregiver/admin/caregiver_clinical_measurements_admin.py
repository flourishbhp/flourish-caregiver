from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from edc_fieldsets import Fieldsets
from edc_fieldsets.fieldlist import Remove
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverClinicalMeasurementsForm
from ..models import CaregiverClinicalMeasurements


@admin.register(CaregiverClinicalMeasurements, site=flourish_caregiver_admin)
class CaregiverClinicalMeasurementsAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = CaregiverClinicalMeasurementsForm

    list_display = ('maternal_visit', 'weight_kg', 'height',
                    'systolic_bp', 'diastolic_bp', 'waist_circ', 'hip_circ')

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'height',
                'weight_kg',
                'systolic_bp',
                'diastolic_bp',
                'confirm_values',
                'waist_circ',
                'hip_circ',
                'all_measurements',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'confirm_values': admin.VERTICAL,
        'all_measurements': admin.VERTICAL}

    @property
    def fu_schedules(self):
        schedules = self.cohort_schedules_cls.objects.filter(
            schedule_type__icontains='followup',
            onschedule_model__startswith='flourish_caregiver').exclude(
                schedule_type__icontains='quarterly').values_list(
                'schedule_name', flat=True)
        return schedules

    @property 
    def conditional_fieldlists(self):
        conditional_fieldlists = {
            '1000M': Remove('waist_circ', 'hip_circ'),
            'a_antenatal1_schedule1': Remove('waist_circ', 'hip_circ'),
            'a_birth1_schedule1': Remove('height', 'waist_circ', 'hip_circ'),
            'tb_2_months_schedule': Remove('height', 'waist_circ', 'hip_circ'), }

        for schedule in self.fu_schedules:
            conditional_fieldlists.update(
                {schedule: Remove('height')})
        return conditional_fieldlists

    def get_keys(self, request, obj=None):
        keys = []

        try:
            model_obj = self.get_instance(request)
        except ObjectDoesNotExist:
            return None
        else:
            if model_obj:
                keys.append(model_obj.schedule_name)

        try:
            visit_obj = self.visit_model.objects.get(id=request.GET.get('maternal_visit'))
        except self.visit_model.DoesNotExist:
            return None
        else:
            keys.append(visit_obj.visit_code)

        return keys

    def get_fieldsets(self, request, obj=None):
        """Returns fieldsets after modifications declared in
        "conditional" dictionaries.
        """
        fieldsets = super().get_fieldsets(request, obj=obj)
        fieldsets = Fieldsets(fieldsets=fieldsets)
        keys = self.get_keys(request, obj)
        for key in keys:
            fieldset = self.conditional_fieldsets.get(key)
            if fieldset:
                try:
                    fieldset = tuple(fieldset)
                except TypeError:
                    fieldset = (fieldset,)
                for f in fieldset:
                    fieldsets.add_fieldset(fieldset=f)
            fieldlist = self.conditional_fieldlists.get(key)
            if fieldlist:
                try:
                    fieldsets.insert_fields(
                        *fieldlist.insert_fields,
                        insert_after=fieldlist.insert_after,
                        section=fieldlist.section)
                except AttributeError:
                    pass
                try:
                    fieldsets.remove_fields(
                        *fieldlist.remove_fields,
                        section=fieldlist.section)
                except AttributeError:
                    pass
        fieldsets = self.update_fieldset_for_form(
            fieldsets, request)
        fieldsets.move_to_end(self.fieldsets_move_to_end)
        return fieldsets.fieldsets
