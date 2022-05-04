from dateutil import relativedelta
from django.apps import apps as django_apps
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base import get_utcnow
from edc_base.utils import age
from edc_constants.constants import NO, POS, YES
from edc_fieldsets import FieldsetsModelAdminMixin, Insert
from edc_model_admin import (
    ModelAdminFormAutoNumberMixin, ModelAdminInstitutionMixin,
    ModelAdminNextUrlRedirectMixin,
    ModelAdminNextUrlRedirectError, ModelAdminReplaceLabelTextMixin)
from edc_model_admin import audit_fieldset_tuple
from edc_visit_schedule.fieldsets import visit_schedule_fieldset_tuple
from edc_visit_tracking.modeladmin_mixins import VisitModelAdminMixin

from .exportaction_mixin import ExportActionMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import MaternalVisitForm
from ..helper_classes import MaternalStatusHelper
from ..models import MaternalVisit


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormAutoNumberMixin,
                      ModelAdminRevisionMixin, ModelAdminReplaceLabelTextMixin,
                      ModelAdminInstitutionMixin, ExportActionMixin,
                      FieldsetsModelAdminMixin):
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
        'tb_participation': admin.VERTICAL,
    }

    def get_key(self, request, obj=None):
        subject_identifier = request.GET.get('subject_identifier')
        try:
            # check for the object were the tb question was captured
            prev_obj = MaternalVisit.objects.get(subject_identifier=subject_identifier,
                                                 tb_participation=YES)
        except MaternalVisit.DoesNotExist:
            # the object does not exist, show the question
            return self.tb_question(subject_identifier)
        else:
            # the object exist so check if it was captured on this visit, show the
            # question if that is true
            if obj and obj.visit_code == prev_obj.visit_code:
                return self.tb_question(subject_identifier)

    def tb_question(self, subject_identifier):
        consent_model = 'subjectconsent'
        tb_consent_model = 'tbinformedconsent'
        antenatal_enrollment_model = 'antenatalenrollment'
        maternal_status_helper = MaternalStatusHelper(
            subject_identifier=subject_identifier)
        consent_model_cls = django_apps.get_model(f'flourish_caregiver.{consent_model}')
        antenatal_enrollment_model_cls = django_apps.get_model(
            f'flourish_caregiver.{antenatal_enrollment_model}')
        tb_consent_model_cls = django_apps.get_model(
            f'flourish_caregiver.{tb_consent_model}')
        consent_obj = consent_model_cls.objects.filter(
            subject_identifier=subject_identifier
        )
        child_subjects = list(consent_obj[0].caregiverchildconsent_set.all().values_list(
            'subject_identifier', flat=True))
        try:
            tb_consent_model_cls.objects.get(subject_identifier=subject_identifier)
        except tb_consent_model_cls.DoesNotExist:
            if (consent_obj and get_difference(consent_obj[0].dob)
                    >= 18 and maternal_status_helper.hiv_status == POS and
                    consent_obj[0].citizen == YES):
                for child_subj in child_subjects:
                    try:
                        antenatal_enrolment_obj = antenatal_enrollment_model_cls.objects.get(
                            subject_identifier=subject_identifier)
                    except antenatal_enrollment_model_cls.DoesNotExist:
                        child_consent = consent_obj[0].caregiverchildconsent_set.get(
                            subject_identifier=child_subj)
                        child_age = age(child_consent.child_dob, get_utcnow())
                        child_age_in_months = (
                                                      child_age.years * 12) + child_age.months
                        if child_age_in_months < 2:
                            return 'tb_2_months'
                    else:
                        if (antenatal_enrolment_obj.ga_lmp_anc_wks and int(
                                antenatal_enrolment_obj.ga_lmp_anc_wks) >= 22):
                            return 'tb_2_months'

    conditional_fieldlists = {
        'tb_2_months': Insert('tb_participation', after='last_alive_date'),
    }
