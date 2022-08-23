from atexit import register
from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from .modeladmin_mixins import CrfModelAdminMixin

from ..models import RelationshipFatherInvolvement
from ..forms import RelationshipFatherInvolvementForm


@register(RelationshipFatherInvolvement, site=flourish_caregiver_admin)
class RelationshipFatherInvolmentAdmin(CrfModelAdminMixin,admin.ModelAdmin):
    
    form = RelationshipFatherInvolvementForm
    
    fieldsets = (
        (None, {
            "fields": (
                'maternal_visit',
                'report_datetime',
                'partner_present',
                'why_partner_upsent',
                'is_partner_the_father',
                'duration_with_partner_months',
                'duration_with_partner_years',
                'partner_age_in_years',
                'living_with_partner',
                'why_not_living_with_partner',
                'disclosure_to_partner',
                'discussion_with_partner',
                'disclose_status',
                'partners_support',
                'ever_separated',
                'times_separated',
                'separation_consideration',
                'after_fight',
                'relationship_progression',
                'confide_in_partner',
                'relationship_regret',
                'quarrel_frequency',
                'bothering_partner',
                'kissing_partner',
                'engage_in_interests',
                'happiness_in_relationship',
                'future_relationship',
                
            ),}
        ),
        ("People involved in taking care of your child", {
            "fields": (
                'father_child_contact',
                'fathers_financial_support',
                'child_left_alone',
                'read_books',
                'told_stories',
                'sang_songs',
                'took_child_outside',
                'played_with_child',
                'named_with_child'
            ),}
        ),
        ("Participiate in study about caregiving", {
            "fields": (
                'interview_participation',
                'contact_info',
                'partner_cell',
            ),}
        ), audit_fieldset_tuple
    )
    
    search_fields = ('subject_identifier',) 
    
    