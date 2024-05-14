from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import ParentAdolRelationshipScaleForm
from ..models import ParentAdolRelationshipScale
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(ParentAdolRelationshipScale, site=flourish_caregiver_admin)
class ParentAdolRelationshipScaleAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = ParentAdolRelationshipScaleForm
    readonly_fields = ('shared_activities',
                       'connectedness',
                       'hostility',)

    fieldsets = (
        (
            'Please read each statement below and rate from 0 (Not At All True) to 5 '
            '(Nearly Always or Always True) how true the statements typically are of your '
            'relationship with your adolescent. There are no right or wrong answers. '
            'Do not spend too much time on any statement. ',
            {
                'fields': [
                    'maternal_visit',
                    'report_datetime',
                    'eat_together',
                    'time_together',
                    'family_events_together',
                    'support_from_others',
                    'show_affection',
                    'comfort',
                    'negative_comments',
                    'compassion',
                    'upset',
                    'play_sport',
                    'complains_about_me',
                    'encourage',
                    'criticize_child',
                    'change_attitude',
                    'encourage_expression',
                    'shared_activities',
                    'connectedness',
                    'hostility',

                ]}
        ), audit_fieldset_tuple)

    radio_fields = {
        'eat_together': admin.HORIZONTAL,
        'time_together': admin.HORIZONTAL,
        'family_events_together': admin.HORIZONTAL,
        'support_from_others': admin.HORIZONTAL,
        'show_affection': admin.HORIZONTAL,
        'comfort': admin.HORIZONTAL,
        'negative_comments': admin.HORIZONTAL,
        'compassion': admin.HORIZONTAL,
        'upset': admin.HORIZONTAL,
        'play_sport': admin.HORIZONTAL,
        'complains_about_me': admin.HORIZONTAL,
        'encourage': admin.HORIZONTAL,
        'criticize_child': admin.HORIZONTAL,
        'change_attitude': admin.HORIZONTAL,
        'encourage_expression': admin.HORIZONTAL
    }
