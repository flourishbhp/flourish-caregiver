from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import HIVDisclosureStatusFormA, HIVDisclosureStatusFormB
from ..forms import HIVDisclosureStatusFormC
from ..models import HIVDisclosureStatusA, HIVDisclosureStatusB
from ..models import HIVDisclosureStatusC

from ..helper_classes.utils import (get_maternal_visit_by_id,
                                    get_child_subject_identifier_by_visit)


class HIVDisclosureStatusAdminMixin(CrfModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'associated_child_identifier',
                'disclosed_status',
                'plan_to_disclose',
                'reason_not_disclosed',
                'reason_not_disclosed_other',
                'disclosure_age',
                'who_disclosed',
                'who_disclosed_other',
                'disclosure_difficulty',
                'child_reaction',
                'child_reaction_other',
                'disclosure_intentional',
                'unintentional_disclosure_reason',
                'unintentional_disclosure_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'disclosed_status': admin.VERTICAL,
                    'reason_not_disclosed': admin.VERTICAL,
                    'who_disclosed': admin.VERTICAL,
                    'disclosure_difficulty': admin.VERTICAL,
                    'child_reaction': admin.VERTICAL,
                    'disclosure_intentional': admin.VERTICAL,
                    'plan_to_disclose': admin.VERTICAL}

    filter_horizontal = ('unintentional_disclosure_reason',)


@admin.register(HIVDisclosureStatusA, site=flourish_caregiver_admin)
class HIVDisclosureStatusAdminA(HIVDisclosureStatusAdminMixin,
                                admin.ModelAdmin):
    form = HIVDisclosureStatusFormA

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)

        maternal_visit_id = initial.get('maternal_visit', None)

        maternal_visit_obj = get_maternal_visit_by_id(
            maternal_visit_id)

        child_identifier = None
        if maternal_visit_obj:
            child_identifier = get_child_subject_identifier_by_visit(
                maternal_visit_obj)

        if child_identifier:
            initial['associated_child_identifier'] = child_identifier
        return initial


@admin.register(HIVDisclosureStatusB, site=flourish_caregiver_admin)
class HIVDisclosureStatusAdminB(HIVDisclosureStatusAdminMixin,
                                admin.ModelAdmin):
    form = HIVDisclosureStatusFormB

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)

        maternal_visit_id = initial.get('maternal_visit', None)

        maternal_visit_obj = get_maternal_visit_by_id(
            maternal_visit_id)

        child_identifier = None
        if maternal_visit_obj:
            child_identifier = get_child_subject_identifier_by_visit(
                maternal_visit_obj)

        if child_identifier:
            post_fix = int(child_identifier[-2:])
            child_identifier = child_identifier[:-2] + str(post_fix + 10)
            initial['associated_child_identifier'] = child_identifier
        return initial


@admin.register(HIVDisclosureStatusC, site=flourish_caregiver_admin)
class HIVDisclosureStatusAdminC(HIVDisclosureStatusAdminMixin,
                                admin.ModelAdmin):
    form = HIVDisclosureStatusFormC

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)

        maternal_visit_id = initial.get('maternal_visit', None)

        maternal_visit_obj = get_maternal_visit_by_id(
            maternal_visit_id)

        child_identifier = None
        if maternal_visit_obj:
            child_identifier = get_child_subject_identifier_by_visit(
                maternal_visit_obj)

        if child_identifier:
            post_fix = int(child_identifier[-3:])
            child_identifier = child_identifier[:-3] + str(post_fix + 20)
            initial['associated_child_identifier'] = child_identifier
        return initial
