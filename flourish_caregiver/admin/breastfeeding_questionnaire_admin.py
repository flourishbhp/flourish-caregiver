from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import BreastFeedingQuestionnaireForm
from ..models import BreastFeedingQuestionnaire
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(BreastFeedingQuestionnaire, site=flourish_caregiver_admin)
class BreastFeedingQuestionnaireAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = BreastFeedingQuestionnaireForm

    fieldsets = (
        (None, {
            "fields": (
                'maternal_visit',
                'report_datetime',
                'feeding_hiv_status',
                'hiv_status_aware',
                'on_hiv_status_aware',
                'hiv_status_during_preg',
                'hiv_status_known_by',
                'father_knew_hiv_status',
                'delivery_advice_vl_results',
                'delivery_advice_on_viralload',
                'after_delivery_advice_vl_results',
                'after_delivery_advice_on_viralload',
                'use_medicines',
                'breastfeeding_duration',
                'during_preg_influencers',
                'during_preg_influencers_other',
                'influenced_during_preg',
                'after_delivery_influencers',
                'after_delivery_influencers_other',
                'influenced_after_delivery',
                'received_training',
                'training_outcome',
                'feeding_advice',
                'community_breastfeeding_bias',
                'community_exclusive_breastfeeding_bias',
                'after_birth_opinion',
                'after_birth_opinion_other',
                'return_to_work_school',
                'returned_to_work_school',
                'six_months_feeding',
                'infant_feeding_reasons',
                'infant_feeding_other',
            ),
        }), audit_fieldset_tuple
    )

    radio_fields = {
        'feeding_hiv_status': admin.VERTICAL,
        'hiv_status_aware': admin.VERTICAL,
        'on_hiv_status_aware': admin.VERTICAL,
        'hiv_status_during_preg': admin.VERTICAL,
        'hiv_status_known_by': admin.VERTICAL,
        'father_knew_hiv_status': admin.VERTICAL,
        'delivery_advice_vl_results': admin.VERTICAL,
        'delivery_advice_on_viralload': admin.VERTICAL,
        'after_delivery_advice_vl_results': admin.VERTICAL,
        'after_delivery_advice_on_viralload': admin.VERTICAL,
        'use_medicines': admin.VERTICAL,
        'breastfeeding_duration': admin.VERTICAL,
        'influenced_during_preg': admin.VERTICAL,
        'influenced_after_delivery': admin.VERTICAL,
        'training_outcome': admin.VERTICAL,
        'community_breastfeeding_bias': admin.VERTICAL,
        'community_exclusive_breastfeeding_bias': admin.VERTICAL,
        'after_birth_opinion': admin.VERTICAL,
        'return_to_work_school': admin.VERTICAL,
        'returned_to_work_school': admin.VERTICAL,
        'six_months_feeding': admin.VERTICAL,
        'feeding_advice': admin.VERTICAL,

    }

    filter_horizontal = ('during_preg_influencers', 'after_delivery_influencers',
                         'received_training', 'infant_feeding_reasons',)
