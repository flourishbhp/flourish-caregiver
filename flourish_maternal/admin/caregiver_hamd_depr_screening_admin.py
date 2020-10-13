from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_maternal_admin
from ..forms import CaregiverHamdDeprScreeningForm
from ..models import CaregiverHamdDeprScreening


@admin.register(CaregiverHamdDeprScreening, site=flourish_maternal_admin)
class CaregiverHamdDeprScreeningAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = CaregiverHamdDeprScreeningForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'depressed_mood',
                'guilt_feelings',
                'suicidal',
                'insomnia_initial',
                'insomnia_middle',
                'insomnia_delayed',
                'work_interests',
                'retardation',
                'agitation',
                'anxiety_pyschic',
                'anxiety',
                'gastro_symptoms',
                'general_symptoms',
                'genital_symptoms',
                'hypochondriasis',
                'weight_loss',
                'insight'
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'depressed_mood': admin.VERTICAL,
                    'guilt_feelings': admin.VERTICAL,
                    'suicidal': admin.VERTICAL,
                    'insomnia_initial': admin.VERTICAL,
                    'insomnia_middle': admin.VERTICAL,
                    'insomnia_delayed': admin.VERTICAL,
                    'work_interests': admin.VERTICAL,
                    'retardation': admin.VERTICAL,
                    'agitation': admin.VERTICAL,
                    'anxiety_pyschic': admin.VERTICAL,
                    'anxiety': admin.VERTICAL,
                    'gastro_symptoms': admin.VERTICAL,
                    'general_symptoms': admin.VERTICAL,
                    'genital_symptoms': admin.VERTICAL,
                    'hypochondriasis': admin.VERTICAL,
                    'weight_loss': admin.VERTICAL,
                    'insight': admin.VERTICAL, }
