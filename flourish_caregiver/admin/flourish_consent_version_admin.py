from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_base.utils import get_utcnow
from edc_fieldsets import FieldsetsModelAdminMixin
from edc_fieldsets.fieldlist import Insert
from edc_model_admin import ModelAdminNextUrlRedirectMixin
from edc_model_admin import audit_fieldset_tuple, ModelAdminNextUrlRedirectError

from ..admin_site import flourish_caregiver_admin
from ..forms import FlourishConsentVersionForm
from ..models import FlourishConsentVersion
from .modeladmin_mixins import ModelAdminMixin


@admin.register(FlourishConsentVersion, site=flourish_caregiver_admin)
class FlourishConsentVersionAdmin(ModelAdminMixin, ModelAdminNextUrlRedirectMixin,
                                  FieldsetsModelAdminMixin,
                                  admin.ModelAdmin):

    form = FlourishConsentVersionForm

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)

        if obj:

            consent_model = django_apps.get_model('flourish_caregiver.subjectconsent')
            preg_screening_cls = django_apps.get_model('flourish_caregiver.screeningpregwomen')
            maternal_dataset_cls = django_apps.get_model(
                'flourish_caregiver.maternaldataset')

            consents = None

            url_name = request.GET.dict().get('next').split(',')[0]
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}

            if request.GET.get('screening_identifier'):
                consents = consent_model.objects.filter(
                    screening_identifier=request.GET.get('screening_identifier'),
                    version=obj.version)

                if consents and request.GET.dict().get('next'):

                    url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')
                    del options['screening_identifier']
                    options['subject_identifier'] = consents[0].subject_identifier

                else:
                    try:
                        maternal_dataset_obj = maternal_dataset_cls.objects.get(
                            screening_identifier=obj.screening_identifier)
                    except maternal_dataset_cls.DoesNotExist:
                        try:
                            preg_screening_cls.objects.get(
                                screening_identifier=obj.screening_identifier)
                        except preg_screening_cls.DoesNotExist:
                            pass
                        else:
                            url_name = settings.DASHBOARD_URL_NAMES.get(
                                'maternal_screening_listboard_url')

                            options['screening_identifier'] = request.GET.get(
                                'screening_identifier')

                    else:
                        del options['screening_identifier']
                        options['study_maternal_identifier'] = maternal_dataset_obj.study_maternal_identifier
                        url_name = settings.DASHBOARD_URL_NAMES.get(
                            'maternal_dataset_listboard_url')

            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')

        return redirect_url

    fieldsets = (
        (None, {
            'fields': [
                'screening_identifier',
                'report_datetime',
                'version',
                'child_version'
                ]}
         ), audit_fieldset_tuple)

    radio_fields = {'version': admin.VERTICAL,
                    'child_version': admin.VERTICAL}

    list_display = ('screening_identifier',
                    'report_datetime',
                    'version',
                    'child_version')

    conditional_fieldlists = {'is_preg': Insert('child_version', after='version')}

    def is_delivery_window(self, subject_identifier):

        maternal_delivery_cls = django_apps.get_model(
            'flourish_caregiver.maternaldelivery')

        try:
            maternal_delivery_obj = maternal_delivery_cls.objects.get(
                subject_identifier=subject_identifier)
        except maternal_delivery_cls.DoesNotExist:
            return True
        else:
            return ((get_utcnow().date() - maternal_delivery_obj.delivery_datetime.date()).days
                    <= 3)

    # def check_if_preg_enroll(self, request, obj=None):
    #
    #     subject_consent_cls = django_apps.get_model(
    #         'flourish_caregiver.subjectconsent')
    #
    #     child_consent_cls = django_apps.get_model(
    #         'flourish_caregiver.caregiverchildconsent')
    #
    #     maternal_delivery_cls = django_apps.get_model(
    #         'flourish_caregiver.maternaldelivery')
    #
    #     preg_screening_cls = django_apps.get_model(
    #         'flourish_caregiver.screeningpregwomen')
    #
    #     try:
    #         screening_preg = preg_screening_cls.objects.get(
    #             screening_identifier=request.GET.get('screening_identifier'))
    #     except preg_screening_cls.DoesNotExist:
    #         latest_subject_consent = subject_consent_cls.objects.filter(
    #             screening_identifier=request.GET.get('screening_identifier')).latest(
    #                 'consent_datetime')
    #     else:
    #         latest_subject_consent = subject_consent_cls.objects.filter(
    #             screening_identifier=screening_preg.screening_identifier).latest(
    #             'consent_datetime')
    #
    #     preg_child_consents = child_consent_cls.objects.filter(
    #             subject_identifier__startswith=latest_subject_consent.subject_identifier,
    #             preg_enroll=True)
    #
    #     if latest_subject_consent and preg_child_consents:
    #
    #         try:
    #             maternal_delivery_cls.objects.get(
    #                 subject_identifier=latest_subject_consent.subject_identifier)
    #         except maternal_delivery_cls.DoesNotExist:
    #             return True
    #         else:
    #             return self.is_delivery_window(latest_subject_consent.subject_identifier)
    #
    #     return False

    # def get_key(self, request, obj=None):
    #
    #     if (obj and obj.child_version) or self.check_if_preg_enroll(request, obj):
    #         return 'is_preg'
