from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

from edc_senaite_interface.admin import SenaiteResultAdminMixin
from edc_model_admin import audit_fieldset_tuple
from edc_fieldsets.fieldlist import Fieldlist, Remove, Insert
from edc_constants.constants import NEG

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverSafiStigmaForm
from ..models import CaregiverSafiStigma
from .modeladmin_mixins import CrfModelAdminMixin
from ..helper_classes import MaternalStatusHelper


@admin.register(CaregiverSafiStigma, site=flourish_caregiver_admin)
class CaregiverSafiStigmaAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverSafiStigmaForm

    fieldsets = (
        ('', {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'judged_negatively',
                'judged_negatively_period',
                'isolated',
                'isolated_period',
                'insulted',
                'insualted_period'
            ]}
         ),
        ('Because someone else in my family has HIV or because I have HIV, I have experienced discrimination at:', {
            'fields': [
                'discriminated_at_home',
                'discriminated_at_home_period',
                'discriminated_at_neigborhood',
                'discriminated_at_neigborhood_period',
                'discriminated_at_religious',
                'discriminated_at_religious_period'
            ]}),

        (' Because someone else in my family has HIV or because I have HIV, discrimination has led my family to: ', {
            'fields': [
                'lose_finacial_support',
                'lose_finacial_support_period',
                'lose_social_support',
                'lose_social_support_period',

            ]}),
        ('Because someone else in my family has HIV or because I have HIV, discrimination has made me feel:', {
            'fields': [
                'stressed_or_anxious',
                'stressed_or_anxious_period',
                'depressed_or_saddened',
                'depressed_or_saddened_period'

            ]}),
        (' ', {
            'fields': [
                'community_hiv_perspective',
                'child_isolated',
                'child_isolated_period',
                'child_insulted',
                'child_insulted_period'

            ]}),
        ('Because of the child’s status, the child has experienced discrimination at:', {
            'fields': [
                'child_home_discrimination',
                'child_home_discrimination_period',
                'child_neighborhood_discrimination',
                'child_neighborhood_discrimination_period',
                'child_religious_place_discrimination',
                'child_religious_place_discrimination_period',
                'child_clinic_discrimination',
                'child_clinic_discrimination_period',
                'child_school_discrimination',
                'child_school_discrimination_period',
                'child_other_discrimination',
                'child_other_discrimination_other',
                'child_other_discrimination_period',

            ]}),

        ('Because of the child’s HIV status, discrimination has negatively affected him/her in the following ways:', {
            'fields': [
                'child_social_effect',
                'child_social_effect_period',
                'child_emotional_effect',
                'child_emotional_effect_period',
                'child_education_effect',
                'child_education_effect_period',
            ]}),
        ('   ', {
            'fields': [
                'child_future_pespective_changed',
                'child_future_pespective_changed_period',

            ]}), audit_fieldset_tuple)

    conditional_fieldlists = {
        NEG: Remove('child_social_effect',
                    'child_social_effect_period',
                    'child_emotional_effect',
                    'child_emotional_effect_period',
                    'child_education_effect',
                    'child_education_effect_period'), }

    def get_key(self, request, obj=None):
        try:
            model_obj = self.get_instance(request)
        except ObjectDoesNotExist:
            return None
        else:
            maternal_visit = getattr(model_obj, 'maternalvisit', None)

            subject_identifier = maternal_visit.subject_identifier

            status_helper = MaternalStatusHelper(subject_identifier=subject_identifier)

            return status_helper.hiv_status

    radio_fields = {
        'judged_negatively': admin.VERTICAL,
        'judged_negatively_period': admin.VERTICAL,
        'isolated': admin.VERTICAL,
        'isolated_period': admin.VERTICAL,
        'insulted': admin.VERTICAL,
        'insualted_period': admin.VERTICAL,
        'discriminated_at_home': admin.VERTICAL,
        'discriminated_at_home_period': admin.VERTICAL,
        'discriminated_at_neigborhood': admin.VERTICAL,
        'discriminated_at_neigborhood_period': admin.VERTICAL,
        'discriminated_at_religious': admin.VERTICAL,
        'discriminated_at_religious_period': admin.VERTICAL,
        'discriminated_at_clinic': admin.VERTICAL,
        'discriminated_at_clinic_period': admin.VERTICAL,
        'discriminated_at_workplace': admin.VERTICAL,
        'discriminated_at_workplace_period': admin.VERTICAL,
        'lose_finacial_support': admin.VERTICAL,
        'lose_finacial_support_period': admin.VERTICAL,
        'lose_social_support': admin.VERTICAL,
        'lose_social_support_period': admin.VERTICAL,
        'stressed_or_anxious': admin.VERTICAL,
        'stressed_or_anxious_period': admin.VERTICAL,
        'depressed_or_saddened': admin.VERTICAL,
        'depressed_or_saddened_period': admin.VERTICAL,
        'community_hiv_perspective': admin.VERTICAL,
        'child_isolated': admin.VERTICAL,
        'child_isolated_period': admin.VERTICAL,
        'child_insulted': admin.VERTICAL,
        'child_insulted_period': admin.VERTICAL,
        'child_home_discrimination': admin.VERTICAL,
        'child_home_discrimination_period': admin.VERTICAL,
        'child_neighborhood_discrimination': admin.VERTICAL,
        'child_neighborhood_discrimination_period': admin.VERTICAL,
        'child_religious_place_discrimination': admin.VERTICAL,
        'child_religious_place_discrimination_period': admin.VERTICAL,
        'child_clinic_discrimination': admin.VERTICAL,
        'child_clinic_discrimination_period': admin.VERTICAL,
        'child_school_discrimination': admin.VERTICAL,
        'child_school_discrimination_period': admin.VERTICAL,
        'child_social_effect': admin.VERTICAL,
        'child_social_effect_period': admin.VERTICAL,
        'child_emotional_effect': admin.VERTICAL,
        'child_emotional_effect_period': admin.VERTICAL,
        'child_education_effect': admin.VERTICAL,
        'child_education_effect_period': admin.VERTICAL,
        'child_future_pespective_changed': admin.VERTICAL,
        'child_future_pespective_changed_period': admin.VERTICAL,
        'child_other_discrimination': admin.VERTICAL,
        'child_other_discrimination_period': admin.VERTICAL,

    }
