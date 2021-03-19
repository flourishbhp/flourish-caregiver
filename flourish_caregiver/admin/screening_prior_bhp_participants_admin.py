from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import ScreeningPriorBhpParticipantsForm
from ..models import ScreeningPriorBhpParticipants


@admin.register(ScreeningPriorBhpParticipants, site=flourish_caregiver_admin)
class ScreeningPriorBhpParticipantsAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ScreeningPriorBhpParticipantsForm

    search_fields = ['study_maternal_identifier', 'screening_identifier']

    fieldsets = (
        (None, {
            'fields': ('screening_identifier',
                       'study_maternal_identifier',
                       'report_datetime',
                       'child_alive',
                       'mother_alive',
                       'flourish_interest',
                       'flourish_participation', )},
         ),
        audit_fieldset_tuple
    )

    radio_fields = {'child_alive': admin.VERTICAL,
                    'mother_alive': admin.VERTICAL,
                    'flourish_interest': admin.VERTICAL,
                    'flourish_participation': admin.VERTICAL}

    list_display = (
        'report_datetime', 'screening_identifier', 'study_maternal_identifier',
        'is_eligible', 'is_consented')

    list_filter = ('report_datetime', 'screening_identifier',
                   'is_eligible', 'is_consented')
