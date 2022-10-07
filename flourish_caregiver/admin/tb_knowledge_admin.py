from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import TbKnowledgeForm
from ..models import TbKnowledge
from .modeladmin_mixins import CrfModelAdminMixin


@admin.register(TbKnowledge, site=flourish_caregiver_admin)
class TbKnowledgeAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = TbKnowledgeForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'tb_informed',
                'tb_knowledge_medium',
                'tb_knowledge_medium_other', ]
            }),
        ('TB Knowledge Section', {
            'fields': [
                'fever_knowledge',
                'cough_knowledge',
                'night_sweats_knowledge',
                'weight_loss_knowledge',
                'rash_knowledge',
                'headache_knowledge',
                'other_knowledge']
        }),
        ('TB Contraction Section', {
            'fields': [
                'tb_utensils_transmit',
                'tb_air_transmit',
                'tb_treatable',
                'tb_curable']
        }),
        audit_fieldset_tuple)

    radio_fields = {'tb_informed': admin.VERTICAL,
                    'fever_knowledge': admin.VERTICAL,
                    'cough_knowledge': admin.VERTICAL,
                    'night_sweats_knowledge': admin.VERTICAL,
                    'weight_loss_knowledge': admin.VERTICAL,
                    'rash_knowledge': admin.VERTICAL,
                    'headache_knowledge': admin.VERTICAL,
                    'tb_utensils_transmit': admin.VERTICAL,
                    'tb_air_transmit': admin.VERTICAL,
                    'tb_treatable': admin.VERTICAL,
                    'tb_curable': admin.VERTICAL, }

    filter_horizontal = ('tb_knowledge_medium',)
