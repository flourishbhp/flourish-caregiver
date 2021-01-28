from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import InPersonContactAttemptForm
from ..models import CaregiverLocator, InPersonContactAttempt


@admin.register(InPersonContactAttempt, site=flourish_caregiver_admin)
class InPersonContactAttemptAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = InPersonContactAttemptForm

    search_fields = ['study_maternal_identifier']

    fieldsets = (
        (None, {
            'fields': ('study_maternal_identifier',
                       'prev_study',
                       'contact_date',
                       'contact_location',
                       'successful_location',
                       'phy_addr_unsuc',
                       'phy_addr_unsuc_other',
                       'workplace_unsuc',
                       'workplace_unsuc_other',
                       'contact_person_unsuc',
                       'contact_person_unsuc_other', )},
         ),
        audit_fieldset_tuple
    )

    radio_fields = {'phy_addr_unsuc': admin.VERTICAL,
                    'workplace_unsuc': admin.VERTICAL,
                    'contact_person_unsuc': admin.VERTICAL}

    list_display = (
        'study_maternal_identifier', 'prev_study', 'contact_date', )

    def get_form(self, request, obj=None, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        custom_choices = []

        study_maternal_identifier = kwargs.get('study_maternal_identifier',
                                               '056-1980010-3')

        fields = self.get_all_fields(form)

        for idx, field in enumerate(fields):
            custom_value = self.custom_field_label(study_maternal_identifier,
                                                   field)

            if custom_value:
                custom_choices.append([field, custom_value])
                form.base_fields[
                    field].label = f'{idx + 1} Why was the in-person visit to {custom_value} unsuccessful?'

        form.custom_choices = custom_choices

        return form

    def custom_field_label(self, study_identifier, field):
        fields_dict = {
            'phy_addr_unsuc': 'physical_address',
            'workplace_unsuc': 'subject_work_place',
            'contact_person_unsuc': 'indirect_contact_physical_address'}

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
        """

        fields = list(instance.base_fields)

        for field in list(instance.declared_fields):
            if field not in fields:
                fields.append(field)
        return fields
