from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_model_admin import (
    ModelAdminFormAutoNumberMixin, ModelAdminInstitutionMixin,
    audit_fieldset_tuple, ModelAdminNextUrlRedirectMixin,
    ModelAdminNextUrlRedirectError, ModelAdminReplaceLabelTextMixin)

from .exportaction_mixin import ExportActionMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import AntenatalEnrollmentForm
from ..models import AntenatalEnrollment


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormAutoNumberMixin,
                      ModelAdminRevisionMixin, ModelAdminReplaceLabelTextMixin,
                      ModelAdminInstitutionMixin):

    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.GET.dict().get('next'):
            url_name = request.GET.dict().get('next').split(',')[0]
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url


@admin.register(AntenatalEnrollment, site=flourish_caregiver_admin)
class AntenatalEnrollmentAdmin(ModelAdminMixin, ExportActionMixin,
                               admin.ModelAdmin):

    form = AntenatalEnrollmentForm

    search_fields = ['subject_identifier']

    fieldsets = (
        (None, {
            'fields': ('subject_identifier',
                       'report_datetime',
                       'knows_lmp',
                       'last_period_date',
                       'edd_by_lmp',
                       'ga_lmp_enrollment_wks',
                       'ga_lmp_anc_wks',
                       'is_diabetic',
                       'will_breastfeed',
                       'will_remain_onstudy',
                       'current_hiv_status',
                       'evidence_hiv_status',
                       'week32_test',
                       'week32_test_date',
                       'week32_result',
                       'evidence_32wk_hiv_status',
                       'will_get_arvs',
                       'rapid_test_done',
                       'rapid_test_date',
                       'rapid_test_result',
                       'enrollment_hiv_status')},
         ),
        audit_fieldset_tuple
    )
    readonly_fields = (
        'edd_by_lmp', 'ga_lmp_enrollment_wks', 'enrollment_hiv_status')
    radio_fields = {'is_diabetic': admin.VERTICAL,
                    'will_breastfeed': admin.VERTICAL,
                    'will_remain_onstudy': admin.VERTICAL,
                    'current_hiv_status': admin.VERTICAL,
                    'week32_test': admin.VERTICAL,
                    'week32_result': admin.VERTICAL,
                    'evidence_32wk_hiv_status': admin.VERTICAL,
                    'evidence_hiv_status': admin.VERTICAL,
                    'will_get_arvs': admin.VERTICAL,
                    'rapid_test_done': admin.VERTICAL,
                    'rapid_test_result': admin.VERTICAL,
                    'knows_lmp': admin.VERTICAL}
    list_display = (
        'subject_identifier', 'report_datetime', 'evidence_hiv_status',
        'will_get_arvs', 'ga_lmp_anc_wks', 'enrollment_hiv_status')
