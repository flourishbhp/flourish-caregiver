from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import InterviewFocusGroupInterestForm
from ..models import InterviewFocusGroupInterest
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(InterviewFocusGroupInterest, site=flourish_caregiver_admin)
class InterviewFocusGroupInterestAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = InterviewFocusGroupInterestForm

    fieldsets = (
        ("In the future, we may conduct smaller studies within FLOURISH that involve discussions. Discussions could "
         "either be one-on-one with a study staff member or in a group with other study participants. We would like "
         "to understand whether you would be interested in participating in discussions, and if so, whether you would "
         "prefer a one-on-one or group discussion. ", {
            "fields": (
                'maternal_visit',
                'report_datetime',
                'discussion_pref',
                'hiv_group_pref',
            ), }
         ),

        ("Some people feel more comfortable talking one-on-one rather than in a group about certain topics. "
         "Do while others may feel more comfortable talking in groups. "
         "We would like to understand your preference in participating in the following topic discussions",
         {
            "fields": (
                'infant_feeding',
                'school_performance',
                'adult_mental_health',
                'child_mental_health',
                'sexual_health',
                'hiv_topics',
                'food_insecurity',
            ), }
         ),
        ("Which of the following topics would you be interested in discussing in a group?",
         {
            "fields": (
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

    search_fields = ('subject_identifier',)
