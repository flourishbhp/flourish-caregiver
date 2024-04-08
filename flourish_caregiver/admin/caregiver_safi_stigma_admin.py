from django.contrib import admin
from django.utils.safestring import mark_safe

from edc_constants.constants import POS
from edc_fieldsets.fieldlist import Remove
from edc_fieldsets.fieldsets import Fieldsets
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverSafiStigmaForm
from ..models import CaregiverSafiStigma
from .modeladmin_mixins import CrfModelAdminMixin
from ..helper_classes import MaternalStatusHelper


@admin.register(CaregiverSafiStigma, site=flourish_caregiver_admin)
class CaregiverSafiStigmaAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverSafiStigmaForm

    fieldsets = [
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'member_lwhiv',
                'judged',
                'judged_period',
                'avoided',
                'avoided_period',
                'insulted',
                'insulted_period'
            ]}
         ),
        ('Because someone else in my family or a close friend has HIV, I have experienced discrimination at:', {
            'fields': [
                'at_home',
                'at_home_period',
                'at_neigborhood',
                'at_neigborhood_period',
                'at_religious',
                'at_religious_period',
                'at_clinic',
                'at_clinic_period',
                'at_workplace',
                'at_workplace_period',
                'other_place',
                'other_place_period'
            ]}),

        ('Because someone else in my family or a close friend has HIV, discrimination has led my family to: ', {
            'fields': [
                'finacial_support',
                'finacial_support_period',
                'social_support',
                'social_support_period',

            ]}),
        ('Because someone else in my family or a close friend has HIV, discrimination has made me feel:', {
            'fields': [
                'stressed',
                'stressed_period',
                'saddened',
                'saddened_period',
                'hiv_perspective'
            ]}),
    ]

    hiv_fieldsets = [
        ('Because of my HIV status, discrimination has negatively affected me in the following ways:', {
            'fields': [
                'social_effect',
                'social_effect_period',
                'emotional_effect',
                'emotional_effect_period',
                'pespective_changed',
                'pespective_changed_period',
        ]},
        ),
    ]
    
    radio_fields = {
        'member_lwhiv': admin.VERTICAL,
        'judged': admin.VERTICAL,
        'judged_period': admin.VERTICAL,
        'avoided': admin.VERTICAL,
        'avoided_period': admin.VERTICAL,
        'insulted': admin.VERTICAL,
        'insulted_period': admin.VERTICAL,
        'at_home': admin.VERTICAL,
        'at_home_period': admin.VERTICAL,
        'at_neigborhood': admin.VERTICAL,
        'at_neigborhood_period': admin.VERTICAL,
        'at_religious': admin.VERTICAL,
        'at_religious_period': admin.VERTICAL,
        'at_clinic': admin.VERTICAL,
        'at_clinic_period': admin.VERTICAL,
        'at_workplace': admin.VERTICAL,
        'at_workplace_period': admin.VERTICAL,
        'finacial_support': admin.VERTICAL,
        'finacial_support_period': admin.VERTICAL,
        'social_support': admin.VERTICAL,
        'social_support_period': admin.VERTICAL,
        'stressed': admin.VERTICAL,
        'stressed_period': admin.VERTICAL,
        'saddened': admin.VERTICAL,
        'saddened_period': admin.VERTICAL,
        'hiv_perspective': admin.VERTICAL,
        'social_effect': admin.VERTICAL,
        'social_effect_period': admin.VERTICAL,
        'emotional_effect': admin.VERTICAL,
        'emotional_effect_period': admin.VERTICAL,
        'pespective_changed': admin.VERTICAL,
        'pespective_changed_period': admin.VERTICAL,
        'other_place_period': admin.VERTICAL,
    }

    conditional_fieldlists = {
        POS: Remove('member_lwhiv')}

    def get_fieldsets(self, request, obj=None):
        """ Returns fieldsets after modifications declared in
            "conditional" dictionaries. Upates also, section label
            for participant's LWHIV.
        """
        fieldsets = list(super().get_fieldsets(request, obj=obj))

        status = self.hiv_status(request)
        if status == POS:
            fieldsets = [
                (self.lwhiv_custom_label(fieldset[0]), {
                    'fields': fieldset[1]['fields']}) for fieldset in fieldsets]
            fieldsets.extend(self.hiv_fieldsets)

        fieldsets.append(audit_fieldset_tuple)
        fieldsets = Fieldsets(fieldsets=fieldsets)
        return fieldsets.fieldsets

    def hiv_status(self, request):
        """ Query hiv status of the participant, uses the maternal status
            helper for the status.
        """
        appointment_obj = self.get_instance(request)
        subject_identifier = getattr(appointment_obj, 'subject_identifier', None)
        status_helper = MaternalStatusHelper(subject_identifier=subject_identifier)
        return getattr(status_helper, 'hiv_status', None)

    def get_key(self, request, obj=None):
        return self.hiv_status(request)

    def update_form_labels(self, request, form):
        """ Update field labels for fields that are common between participant's
            LWHIV and not-LWHIV, respective to the HIV status of the participant.
            NOTE: Applicable to fields on the first section only.
        """
        form = super().update_form_labels(request, form)

        if self.hiv_status(request) == POS:
            for fieldset in self.fieldsets:
                section, fields_dict = fieldset
                fields = fields_dict.get('fields', []) if not bool(section) else []
                for field in fields:
                    self.update_field_labels(form, field)
        return form

    def update_field_labels(self, form, field):
        if field not in ('member_lwhiv', 'hiv_perspective', ):
            form_field = form.base_fields.get(field, None)
            label = getattr(form_field, 'label', '')
            label = self.lwhiv_custom_label(label)
            form_field.label = mark_safe(label)

    def lwhiv_custom_label(self, str_text):
        replace_text = 'Because I have HIV, '
        parts = str_text.split(',', 1) if str_text else []
        if len(parts) == 2:
            str_text = replace_text + parts[1]
        return str_text
