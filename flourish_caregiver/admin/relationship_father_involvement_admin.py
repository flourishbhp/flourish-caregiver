from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import RelationshipFatherInvolvementForm
from ..models import RelationshipFatherInvolvement
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(RelationshipFatherInvolvement, site=flourish_caregiver_admin)
class RelationshipFatherInvolvementAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = RelationshipFatherInvolvementForm

    fieldsets = (
        (None, {
            "fields": (
                'maternal_visit',
                'report_datetime',
                'partner_present',
                'why_partner_absent',
                'is_partner_the_father',
                'duration_with_partner',
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
                'leave_after_fight',
                'relationship_progression',
                'confide_in_partner',
                'relationship_regret',
                'quarrel_frequency',
                'bothering_partner',
                'kissing_partner',
                'engage_in_interests',
                'happiness_in_relationship',
                'future_relationship',

            ), }
         ),
        ("People involved in taking care of your child", {
            "fields": (
                'biological_father_alive',
                'father_child_contact',
                'fathers_financial_support',
                'child_left_alone',
            ), }
         ),
        ("In the past 3 days, did you or any household member aged 15 or over engage"
         " in any of the following activities with the child", {
            "fields": (
                'read_books',
                'read_books_other',
                'told_stories',
                'told_stories_other',
                'sang_songs',
                'sang_songs_other',
                'took_child_outside',
                'took_child_outside_other',
                'played_with_child',
                'played_with_child_other',
                'named_with_child',
                'named_with_child_other'
            ), }
         ),
        ("Participiate in study about caregiving", {
            "fields": (
                'interview_participation',
                'contact_info',
                'partner_cell',
                'conunselling_referral'
            ), }
         ), audit_fieldset_tuple
    )

    search_fields = ('maternal_visit__subject_identifier',)

    radio_fields = {'partner_present': admin.VERTICAL,
                    'biological_father_alive': admin.VERTICAL,
                    'is_partner_the_father': admin.VERTICAL,
                    'living_with_partner': admin.VERTICAL,
                    'disclosure_to_partner': admin.VERTICAL,
                    'discussion_with_partner': admin.VERTICAL,
                    'disclose_status': admin.VERTICAL,
                    'partners_support': admin.VERTICAL,
                    'ever_separated': admin.VERTICAL,
                    'separation_consideration': admin.VERTICAL,
                    'leave_after_fight': admin.VERTICAL,
                    'relationship_progression': admin.VERTICAL,
                    'confide_in_partner': admin.VERTICAL,
                    'relationship_regret': admin.VERTICAL,
                    'quarrel_frequency': admin.VERTICAL,
                    'bothering_partner': admin.VERTICAL,
                    'kissing_partner': admin.VERTICAL,
                    'engage_in_interests': admin.VERTICAL,
                    'happiness_in_relationship': admin.VERTICAL,
                    'future_relationship': admin.VERTICAL,
                    'father_child_contact': admin.VERTICAL,
                    'fathers_financial_support': admin.VERTICAL,
                    'interview_participation': admin.VERTICAL,
                    'contact_info': admin.VERTICAL,
                    'conunselling_referral': admin.VERTICAL, }

    filter_horizontal = (
        'read_books', 'told_stories', 'sang_songs', 'took_child_outside',
        'played_with_child', 'named_with_child')
