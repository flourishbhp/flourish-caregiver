from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import ModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import TbPresenceHouseholdMembersForm
from ..models import TbPresenceHouseholdMembers


@admin.register(TbPresenceHouseholdMembers, site=flourish_caregiver_admin)
class TbPresenceHouseholdMembersAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = TbPresenceHouseholdMembersForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'tb_diagnosed',
                'tb_ind_rel',
                'tb_ind_other',
                'cough_signs',
                'cough_ind_rel',
                'cough_ind_other',
                'fever_signs',
                'fever_ind_rel',
                'fever_ind_other',
                'night_sweats',
                'sweat_ind_rel',
                'sweat_ind_other',
                'weight_loss',
                'weight_ind_rel',
                'weight_ind_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'tb_diagnosed': admin.VERTICAL,
                    'tb_ind_rel': admin.VERTICAL,
                    'cough_signs': admin.VERTICAL,
                    'cough_ind_rel': admin.VERTICAL,
                    'fever_signs': admin.VERTICAL,
                    'fever_ind_rel': admin.VERTICAL,
                    'night_sweats': admin.VERTICAL,
                    'sweat_ind_rel': admin.VERTICAL,
                    'weight_loss': admin.VERTICAL,
                    'weight_ind_rel': admin.VERTICAL}
