from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.safestring import mark_safe
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.sites.admin import ModelAdminSiteMixin
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_metadata import NextFormGetter
from edc_model_admin import (FormAsJSONModelAdminMixin, ModelAdminAuditFieldsMixin,
                             ModelAdminFormAutoNumberMixin,
                             ModelAdminFormInstructionsMixin, ModelAdminInstitutionMixin,
                             ModelAdminNextUrlRedirectMixin, ModelAdminReadOnlyMixin,
                             ModelAdminRedirectOnDeleteMixin)
from edc_visit_tracking.modeladmin_mixins import (
    CrfModelAdminMixin as VisitTrackingCrfModelAdminMixin)

from .exportaction_mixin import ExportActionMixin
from ..models.cohort_schedules import CohortSchedules


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin,
                      ModelAdminRedirectOnDeleteMixin,
                      ModelAdminSiteMixin,
                      ExportActionMixin):
    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'
    next_form_getter_cls = NextFormGetter


class CrfModelAdminMixin(VisitTrackingCrfModelAdminMixin,
                         ModelAdminMixin,
                         FieldsetsModelAdminMixin,
                         FormAsJSONModelAdminMixin,
                         admin.ModelAdmin):
    show_save_next = True
    show_cancel = True

    post_url_on_delete_name = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')

    @property
    def cohort_schedules_cls(self):
        model_name = 'flourish_caregiver.cohortschedules'
        return django_apps.get_model(model_name)

    def post_url_on_delete_kwargs(self, request, obj):
        return dict(
            subject_identifier=obj.maternal_visit.subject_identifier,
            appointment=str(obj.maternal_visit.appointment.id))

    def view_on_site(self, obj):
        dashboard_url_name = settings.DASHBOARD_URL_NAMES.get(
            'subject_dashboard_url')
        try:
            url = reverse(
                dashboard_url_name, kwargs=dict(
                    subject_identifier=obj.maternal_visit.subject_identifier,
                    appointment=str(obj.maternal_visit.appointment.id)))
        except NoReverseMatch:
            url = super().view_on_site(obj)
        return url

    def get_appointment(self, request):
        """Returns the appointment instance for this request or None.
        """
        appointment_model_cls = django_apps.get_model(self.appointment_model)
        return appointment_model_cls.objects.get(
            pk=request.GET.get('appointment'))
        return None

    def get_previous_instance(self, request, instance=None, **kwargs):
        """Returns a model instance that is the first occurrence of a previous
        instance relative to this object's appointment.
        """
        obj = None
        appointment = instance or self.get_instance(request)
        if appointment:
            while appointment:
                options = {
                    '{}__appointment'.format(self.model.visit_model_attr()):
                        self.get_previous_appt_instance(appointment)
                }
                try:
                    obj = self.model.objects.get(**options)
                except ObjectDoesNotExist:
                    pass
                else:
                    break
                appointment = self.get_previous_appt_instance(appointment)
        return obj

    def get_previous_appt_instance(self, appointment):
        try:
            appointment = appointment.__class__.objects.filter(
                subject_identifier=appointment.subject_identifier,
                visit_schedule_name=appointment.visit_schedule_name,
                schedule_name__endswith=appointment.schedule_name[-11:],
                timepoint_datetime__lt=appointment.timepoint_datetime,
                visit_code_sequence=0).latest('timepoint_datetime')
        except appointment.__class__.DoesNotExist:
            return self.get_previous_by_appt_datetime(appointment)
        else:
            return appointment

    def get_schedule_names(self, appointment):
        try:
            cohort_schedules = CohortSchedules.objects.get(
                schedule_name=appointment.schedule_name)
        except CohortSchedules.DoesNotExist:
            return []
        else:
            child_count = getattr(
                cohort_schedules, 'child_count', None)
            names = CohortSchedules.objects.filter(
                child_count=child_count,
                onschedule_model__startswith='flourish_caregiver').values_list(
                'schedule_name', flat=True).exclude(
                Q(schedule_name__icontains='tb') | Q(schedule_name__icontains='facet'))
            return names

    def get_previous_by_appt_datetime(self, appointment):
        try:
            prev_appt = appointment.__class__.objects.filter(
                subject_identifier=appointment.subject_identifier,
                schedule_name__in=self.get_schedule_names(appointment),
                appt_datetime__lt=appointment.appt_datetime).latest(
                'appt_datetime')
        except appointment.__class__.DoesNotExist:
            return None
        else:
            return prev_appt

    def get_instance(self, request):
        try:
            appointment = self.get_appointment(request)
        except ObjectDoesNotExist:
            return None
        else:
            return appointment

    def get_key(self, request, obj=None):
        schedule_name = None
        if self.get_previous_instance(request):
            try:
                model_obj = self.get_instance(request)
            except ObjectDoesNotExist:
                schedule_name = None
            else:
                schedule_name = model_obj.schedule_name
        return schedule_name


class VersionControlMixin:

    def get_form_version(self, request):

        form_versions = django_apps.get_app_config(
            'flourish_caregiver').form_versions

        queryset = self.get_queryset(request)
        model_name = queryset.model._meta.label_lower
        form_version = form_versions.get(model_name)

        return mark_safe(
            f' Version: {form_version} ')

    def get_timepoint(self, request):

        appt_model = django_apps.get_model('edc_appointment.appointment')

        try:
            app_obj = appt_model.objects.get(id=request.GET.get('appointment'))
        except appt_model.DoesNotExist:
            pass
        else:
            return mark_safe(
                f'Timepoint: <i>{app_obj.visits.get(app_obj.visit_code).title} '
                '</i> &emsp; ')
