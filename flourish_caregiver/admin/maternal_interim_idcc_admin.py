from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from flourish_caregiver.models.maternal_hiv_interim_hx import MaternalHivInterimHx

from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalInterimIdccForm
from ..models import MaternalInterimIdcc
from .modeladmin_mixins import CrfModelAdminMixin
from django.utils.safestring import mark_safe

@admin.register(MaternalInterimIdcc, site=flourish_caregiver_admin)
class MaternalInterimIdccAdmin(CrfModelAdminMixin, admin.ModelAdmin):

    form = MaternalInterimIdccForm
    change_form_template = 'admin/flourish_caregiver/maternalinterimidcc/change_form.html'
    add_form_template = 'admin/flourish_caregiver/maternalinterimidcc/change_form.html'

    list_display = ('maternal_visit', 'report_datetime',
                    'recent_cd4', 'value_vl',)

    list_filter = (
        'info_since_lastvisit', 'recent_cd4_date',
        'value_vl_size', 'recent_vl_date')

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'info_since_lastvisit',
                'recent_cd4',
                'recent_cd4_date',
                'value_vl_size',
                'value_vl',
                'recent_vl_date',
                'other_diagnoses']}
         ), audit_fieldset_tuple)

    radio_fields = {'info_since_lastvisit': admin.VERTICAL,
                    'value_vl_size': admin.VERTICAL}
    
    def get_model_data(self, request,object_id):
        
        subject_identifier=''
        
        try:
            subject_identifier = request.GET.get('subject_identifier')
        except Exception:
            pass
        else:
            subject_identifier = self.get_object(request, object_id).maternal_visit.subject_identifier    
               
        # get the hiv interim history
        try:
            interimHx = MaternalHivInterimHx.objects.get(maternal_visit__subject_identifier=subject_identifier)
        except MaternalHivInterimHx.DoesNotExist:
            pass
        else:
            return interimHx
    
    def add_interimhx(self, request, object_id,extra_context=None):
        extra_context = extra_context or {}
        extra_context[
            'interimhx'] = self.get_model_data(request,object_id)
        return extra_context

    def add_view(self, request, object_id,form_url='', extra_context=None):
        extra_context = self.add_interimhx(request,object_id)
        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = self.add_interimhx(request,object_id)
        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
