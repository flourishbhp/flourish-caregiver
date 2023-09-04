from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import PhoneCallContactForm
from ..models import PhoneCallContact, CaregiverLocator


@admin.register(PhoneCallContact, site=flourish_caregiver_admin)
class PhoneCallContactAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = PhoneCallContactForm

    search_fields = ['study_maternal_identifier']

    fieldsets = (
        (None, {
            'fields': ('study_maternal_identifier',
                       'prev_study',
                       'contact_date',
                       'phone_num_type',
                       'phone_num_success',
                       'cell_contact_fail',
                       'alt_cell_contact_fail',
                       'tel_contact_fail',
                       'alt_tel_contact_fail',
                       'work_contact_fail',
                       'cell_alt_contact_fail',
                       'tel_alt_contact_fail',
                       'cell_resp_person_fail',
                       'tel_resp_person_fail', )},
         ),
        audit_fieldset_tuple
    )

    radio_fields = {'cell_contact_fail': admin.VERTICAL,
                    'alt_cell_contact_fail': admin.VERTICAL,
                    'tel_contact_fail': admin.VERTICAL,
                    'alt_tel_contact_fail': admin.VERTICAL,
                    'work_contact_fail': admin.VERTICAL,
                    'cell_alt_contact_fail': admin.VERTICAL,
                    'tel_alt_contact_fail': admin.VERTICAL,
                    'cell_resp_person_fail': admin.VERTICAL,
                    'tel_resp_person_fail': admin.VERTICAL}

    list_display = (
        'study_maternal_identifier', 'prev_study', 'contact_date', )

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        custom_choices = []

        study_maternal_identifier = kwargs.get(
            'study_maternal_identifier', 'B003611-4')

        fields = self.get_all_fields(form)

        for idx, field in enumerate(fields):
            custom_value = self.custom_field_label(
                study_maternal_identifier, field)

            if custom_value:
                custom_choices.append([field, custom_value])
                form.base_fields[field].label = f'{idx + 1} Why was the contact to {custom_value} unsuccessful?'
        form.custom_choices = custom_choices
#             else:
#                 fields_exclude.append(field)
#         fields = [field for field in self.fieldsets[0][1].get('fields') not in fields_exclude]
#         self.fieldsets[0][1]('fields') = tuple(fields)

        return form

    def custom_field_label(self, study_identifier, field):
        fields_dict = {
            'cell_contact_fail': 'subject_cell',
            'alt_cell_contact_fail': 'subject_cell_alt',
            'tel_contact_fail': 'subject_phone',
            'alt_tel_contact_fail': 'subject_phone_alt',
            'work_contact_fail': 'subject_work_phone',
            'cell_alt_contact_fail': 'indirect_contact_cell',
            'tel_alt_contact_fail': 'indirect_contact_phone',
            'cell_resp_person_fail': 'caretaker_cell',
            'tel_resp_person_fail': 'caretaker_tel'}

        try:
            locator_obj = CaregiverLocator.objects.get(
                study_maternal_identifier=study_identifier)
        except CaregiverLocator.DoesNotExist:
            pass
        else:
            attr_name = fields_dict.get(field, None)
            if attr_name:
                return getattr(locator_obj, attr_name, '')

    def get_all_fields(self, instance):
        """"
        Return names of all available fields from given Form instance.

        :arg instance: Form instance
        :returns list of field names
        :rtype: list
        """

        fields = list(instance.base_fields)

        for field in list(instance.declared_fields):
            if field not in fields:
                fields.append(field)
        return fields
