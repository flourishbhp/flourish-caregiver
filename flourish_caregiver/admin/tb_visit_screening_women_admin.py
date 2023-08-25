from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from flourish_caregiver.admin.modeladmin_mixins import CrfModelAdminMixin
from flourish_caregiver.admin_site import flourish_caregiver_admin
from flourish_caregiver.forms import TbVisitScreeningWomenForm
from flourish_caregiver.models import TbVisitScreeningWomen


@admin.register(TbVisitScreeningWomen, site=flourish_caregiver_admin)
class TbVisitScreeningWomenAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = TbVisitScreeningWomenForm

    fieldsets = (
        (None, {
            'fields': (
                'maternal_visit',
                'report_datetime',
            )}
         ), ('Cough', {
             'fields': (
                 'have_cough',
                 'cough_duration',
                 'cough_intersects_preg',
                 'cough_num',
                 'cough_duration_preg',
                 'seek_med_help',
                 'cough_illness',
                 'cough_illness_times',
                 'cough_illness_preg',
                 'cough_illness_med_help',
             )}), ('Fever', {
                 'fields': (
                     'fever',
                     'fever_during_preg',
                     'fever_illness_times',
                     'fever_illness_preg',
                     'fever_illness_postpartum',
                     'fever_illness_postpartum_times',
                     'fever_illness_postpartum_preg',
                 )}), ('Night Sweats', {
                     'fields': (
                         'night_sweats',
                         'night_sweats_during_preg',
                         'night_sweats_during_preg_times',
                         'night_sweats_during_preg_clinic',
                         'night_sweats_postpartum',
                         'night_sweats_postpartum_times',
                         'night_sweats_postpartum_clinic',
                     )}), ('Weight Loss', {
                         'fields': (
                             'weight_loss',
                             'weight_loss_during_preg',
                             'weight_loss_during_preg_times',
                             'weight_loss_during_preg_clinic',
                             'weight_loss_postpartum',
                             'weight_loss_postpartum_times',
                             'weight_loss_postpartum_clinic',
                         )}), ('Cough Blood', {
                             'fields': (
                                 'cough_blood',
                                 'cough_blood_during_preg',
                                 'cough_blood_during_preg_times',
                                 'cough_blood_during_preg_clinic',
                                 'cough_blood_postpartum',
                                 'cough_blood_postpartum_times',
                                 'cough_blood_postpartum_clinic',
                             )}), ('Enlarged Lymph Nodes', {
                                 'fields': (
                                     'enlarged_lymph_nodes',
                                     'enlarged_lymph_nodes_during_preg',
                                     'enlarged_lymph_nodes_during_preg_times',
                                     'enlarged_lymph_nodes_during_preg_clinic',
                                     'enlarged_lymph_nodes_postpartum',
                                     'enlarged_lymph_nodes_postpartum_times',
                                     'enlarged_lymph_nodes_postpartum_clinic',
                                 )}), ('Unexplained Fatigue', {
                                     'fields': (
                                         'unexplained_fatigue',
                                         'unexplained_fatigue_during_preg',
                                         'unexplained_fatigue_during_preg_times',
                                         'unexplained_fatigue_during_preg_clinic',
                                         'unexplained_fatigue_postpartum',
                                         'unexplained_fatigue_postpartum_times',
                                         'unexplained_fatigue_postpartum_clinic',
                                     )}), ('Tb Referral', {
                                         'fields': (
                                             'tb_referral',
                                         )}),
        audit_fieldset_tuple
    )

    radio_fields = {
        'have_cough': admin.VERTICAL,
        'cough_duration': admin.VERTICAL,
        'cough_intersects_preg': admin.VERTICAL,
        'cough_duration_preg': admin.VERTICAL,
        'seek_med_help': admin.VERTICAL,
        'cough_illness': admin.VERTICAL,
        'cough_illness_preg': admin.VERTICAL,
        'cough_illness_med_help': admin.VERTICAL,
        'fever': admin.VERTICAL,
        'fever_during_preg': admin.VERTICAL,
        'fever_illness_preg': admin.VERTICAL,
        'fever_illness_postpartum': admin.VERTICAL,
        'fever_illness_postpartum_preg': admin.VERTICAL,
        'night_sweats': admin.VERTICAL,
        'night_sweats_during_preg': admin.VERTICAL,
        'night_sweats_during_preg_clinic': admin.VERTICAL,
        'night_sweats_postpartum': admin.VERTICAL,
        'night_sweats_postpartum_clinic': admin.VERTICAL,
        'weight_loss': admin.VERTICAL,
        'weight_loss_during_preg': admin.VERTICAL,
        'weight_loss_during_preg_clinic': admin.VERTICAL,
        'weight_loss_postpartum': admin.VERTICAL,
        'weight_loss_postpartum_clinic': admin.VERTICAL,
        'cough_blood': admin.VERTICAL,
        'cough_blood_during_preg': admin.VERTICAL,
        'cough_blood_during_preg_clinic': admin.VERTICAL,
        'cough_blood_postpartum': admin.VERTICAL,
        'cough_blood_postpartum_clinic': admin.VERTICAL,
        'enlarged_lymph_nodes': admin.VERTICAL,
        'enlarged_lymph_nodes_during_preg': admin.VERTICAL,
        'enlarged_lymph_nodes_during_preg_clinic': admin.VERTICAL,
        'enlarged_lymph_nodes_postpartum': admin.VERTICAL,
        'enlarged_lymph_nodes_postpartum_clinic': admin.VERTICAL,
        'unexplained_fatigue': admin.VERTICAL,
        'unexplained_fatigue_during_preg': admin.VERTICAL,
        'unexplained_fatigue_during_preg_clinic': admin.VERTICAL,
        'unexplained_fatigue_postpartum': admin.VERTICAL,
        'unexplained_fatigue_postpartum_clinic': admin.VERTICAL,
        'tb_referral': admin.VERTICAL,
    }
