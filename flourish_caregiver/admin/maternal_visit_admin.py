from dateutil import relativedelta
from django.apps import apps as django_apps
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base import get_utcnow
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_constants.constants import NO, NOT_APPLICABLE
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_fieldsets.fieldlist import Insert
from edc_model_admin import (
    ModelAdminFormAutoNumberMixin, ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin, ModelAdminAuditFieldsMixin,
    ModelAdminNextUrlRedirectError, ModelAdminReplaceLabelTextMixin)
from edc_model_admin import audit_fieldset_tuple

from edc_visit_schedule.fieldsets import visit_schedule_fieldset_tuple
from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalVisitForm
from ..models import MaternalVisit
from .exportaction_mixin import ExportActionMixin


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormAutoNumberMixin,
                      ModelAdminRevisionMixin, ModelAdminReplaceLabelTextMixin,
                      ModelAdminInstitutionMixin, ExportActionMixin,
                      ModelAdminAuditFieldsMixin, FieldsetsModelAdminMixin,
                      ModelAdminSiteMixin):

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
            if (obj.require_crfs == NO):
                del options['appointment']
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url


def get_difference(birth_date=None):
    difference = relativedelta.relativedelta(
        get_utcnow().date(), birth_date)
    return difference.years


@admin.register(MaternalVisit, site=flourish_caregiver_admin)
class MaternalVisitAdmin(ModelAdminMixin, VisitModelAdminMixin,
                         admin.ModelAdmin):
    form = MaternalVisitForm

    fieldsets = (
        (None, {
            'fields': [
                'appointment',
                'report_datetime',
                'reason',
                'reason_missed',
                'study_status',
                'info_source',
                'info_source_other',
                'is_present',
                'survival_status',
                'last_alive_date',
                'comments'
            ]
        }),
        visit_schedule_fieldset_tuple,
        audit_fieldset_tuple
    )

    radio_fields = {
        'reason': admin.VERTICAL,
        'study_status': admin.VERTICAL,
        'info_source': admin.VERTICAL,
        'is_present': admin.VERTICAL,
        'survival_status': admin.VERTICAL,
        'brain_scan': admin.VERTICAL
    }

    conditional_fieldlists = {
        'interested_in_brain_scan': Insert('brain_scan', after='survival_status')
    }

    @property
    def appointment_model_cls(self):

        return django_apps.get_model(self.appointment_model)

    def get_key(self, request, obj=None):

        key = super().get_key(request, obj)

        subject_identifier = (request.GET.get('subject_identifier', None)
                              or request.POST.get('subject_identifier', None))

        try:

            enrollment_visit = self.model.objects.get(
                    subject_identifier=subject_identifier,
                    visit_code='1000M',
                    visit_code_sequence='1')

        except self.model.DoesNotExist:
            """
            1000M visit doen't exist, check if the current vist yet to be saved
            is visit 1000M
            """
            appointment_id = (request.GET.get('appointment', None)
                              or request.POST.get('appointment', None))
            try:
                self.appointment_model_cls.objects.get(id=appointment_id,
                                                       visit_code='1000M',
                                                       visit_code_sequence='1')

            except self.appointment_model_cls.DoesNotExist:
                pass
            else:
                key = 'interested_in_brain_scan'

        else:
            """
            If previous visit does exist, and if response is brain_scan == NO
            or NOT_APPLICABLE and current visit is 2000D show brain scan option
            """

            if (enrollment_visit.brain_scan in [NO, NOT_APPLICABLE]
                    and enrollment_visit.visit_code in ['2000D', '1000M']):

                key = 'interested_in_brain_scan'

        return key
