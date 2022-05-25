from django.apps import apps as django_apps
from django.contrib import admin
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_fieldsets.fieldlist import Insert
from edc_model_admin import audit_fieldset_tuple

from ..admin_site import flourish_caregiver_admin
from ..forms import FlourishConsentVersionForm
from ..models import FlourishConsentVersion
from .modeladmin_mixins import ModelAdminMixin


@admin.register(FlourishConsentVersion, site=flourish_caregiver_admin)
class FlourishConsentVersionAdmin(ModelAdminMixin,
                                  FieldsetsModelAdminMixin,
                                  admin.ModelAdmin):

    form = FlourishConsentVersionForm

    fieldsets = (
        (None, {
            'fields': [
                'screening_identifier',
                'report_datetime',
                'version',
                ]}
         ), audit_fieldset_tuple)

    radio_fields = {'version': admin.VERTICAL,
                    'child_version': admin.VERTICAL}

    list_display = ('screening_identifier',
                    'report_datetime',
                    'version',)

    conditional_fieldlists = {'is_preg': Insert('child_version', after='version')}

    def check_if_preg_enroll(self, request, obj=None):

        subject_consent_cls = django_apps.get_model(
            'flourish_caregiver.subjectconsent')

        child_consent_cls = django_apps.get_model(
            'flourish_caregiver.caregiverchildconsent')

        maternal_delivery_cls = django_apps.get_model(
            'flourish_caregiver.maternaldelivery')

        preg_screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpregwomen')

        try:
            screening_preg = preg_screening_cls.objects.get(
                screening_identifier=request.GET.get('screening_identifier'))
        except preg_screening_cls.DoesNotExist:
            latest_subject_consent = subject_consent_cls.objects.filter(
                screening_identifier=request.GET.get('screening_identifier')).latest(
                    'consent_datetime')
        else:
            latest_subject_consent = subject_consent_cls.objects.filter(
                screening_identifier=screening_preg.screening_identifier).latest(
                'consent_datetime')

        preg_child_consents = child_consent_cls.objects.filter(
                subject_identifier__startswith=latest_subject_consent.subject_identifier,
                preg_enroll=True)

        if latest_subject_consent and preg_child_consents:

            try:
                maternal_delivery_cls.objects.get(
                    subject_identifier=latest_subject_consent.subject_identifier)
            except maternal_delivery_cls.DoesNotExist:
                return True

        return False

    def get_key(self, request, obj=None):

        if (obj and obj.child_version) or self.check_if_preg_enroll(request, obj):
            return 'is_preg'
