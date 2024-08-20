from django.contrib import admin
from django.utils.safestring import mark_safe
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import InterviewFocusGroupInterestForm
from ..models import InterviewFocusGroupInterest


@admin.register(InterviewFocusGroupInterest, site=flourish_caregiver_admin)
class InterviewFocusGroupInterestAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = InterviewFocusGroupInterestForm

    additional_instructions = mark_safe(
        '<b>***INSTRUCTIONS CLINIC STAFF: The questions I will ask are designed '
        'solely for data collection purposes and the purpose of these questions is '
        'to explore your topic of interest for discussion in case we are to have '
        'interviews or focus group settings, in our future studies. At this time, '
        'there are no ongoing or upcoming studies to address these interests '
        'however, your responses will help to identify future study topics.</b>')

    fieldsets = (
        (
            None, {
                "fields": (
                    'maternal_visit',
                    'report_datetime',
                    'discussion_pref',
                    'hiv_group_pref',
                ), }
        ),

        (
            "Some people feel more comfortable talking one-on-one rather than in a group "
            "about certain topics. "
            "Do while others may feel more comfortable talking in groups. "
            "We would like to understand your preference in participating in the "
            "following "
            "topic discussions",
            {
                "fields": (
                    'infant_feeding',
                    'school_performance',
                    'adult_mental_health',
                    'child_mental_health',
                    'sexual_health',
                    'hiv_topics',
                    'food_insecurity',
                    'wellness',
                    'non_comm_diseases',
                    'social_issues',
                    'covid19',
                    'vaccines',
                    'infant_feeding_group_interest',
                    'same_status_comfort',
                    'diff_status_comfort',
                ), }
        ),

        ("Additional Topics",
         {
             "fields": (
                 'women_discussion_topics',
                 'adolescent_discussion_topics',
             ), }
         ), audit_fieldset_tuple
    )

    radio_fields = {
        'discussion_pref': admin.VERTICAL,
        'hiv_group_pref': admin.VERTICAL,
        'infant_feeding': admin.VERTICAL,
        'school_performance': admin.VERTICAL,
        'adult_mental_health': admin.VERTICAL,
        'child_mental_health': admin.VERTICAL,
        'sexual_health': admin.VERTICAL,
        'hiv_topics': admin.VERTICAL,
        'food_insecurity': admin.VERTICAL,
        'wellness': admin.VERTICAL,
        'non_comm_diseases': admin.VERTICAL,
        'social_issues': admin.VERTICAL,
        'covid19': admin.VERTICAL,
        'vaccines': admin.VERTICAL,
        'infant_feeding_group_interest': admin.VERTICAL,
        'same_status_comfort': admin.VERTICAL,
        'diff_status_comfort': admin.VERTICAL,
    }

    search_fields = ('maternal_visit__subject_identifier',)
