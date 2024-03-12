from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_model_admin import audit_fieldset_tuple, ModelAdminFormAutoNumberMixin, \
    ModelAdminNextUrlRedirectError, \
    StackedInlineMixin

from .modeladmin_mixins import ModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import ScreeningPregWomenForm
from ..forms.screening_preg_women_form import ScreeningPregWomenInlineForm
from ..models import ScreeningPregWomen
from ..models.screening_preg_women import ScreeningPregWomenInline


# Introducing BaseScreeningPregWomenAdmin class to reduce repetition
class BaseScreeningPregWomenAdmin:
    form = ScreeningPregWomenInlineForm
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('child_subject_identifier',
                       'report_datetime',
                       'hiv_testing',)},
         ),
        audit_fieldset_tuple
    )
    radio_fields = {'hiv_testing': admin.VERTICAL, }


@admin.register(ScreeningPregWomenInline, site=flourish_caregiver_admin)
class ScreeningPregWomenInlineAdmin(BaseScreeningPregWomenAdmin, admin.ModelAdmin):
    pass


class ScreeningPregWomenInline(BaseScreeningPregWomenAdmin, StackedInlineMixin,
                               ModelAdminFormAutoNumberMixin, admin.StackedInline, ):
    model = ScreeningPregWomenInline


@admin.register(ScreeningPregWomen, site=flourish_caregiver_admin)
class ScreeningPregWomenAdmin(ModelAdminMixin, admin.ModelAdmin):
    form = ScreeningPregWomenForm

    search_fields = ['screening_identifier']

    inlines = [ScreeningPregWomenInline, ]

    fieldsets = (
        (None, {
            'fields': ('screening_identifier',)},
         ),
        audit_fieldset_tuple
    )

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)

        consent_model = django_apps.get_model(
            'flourish_caregiver.subjectconsent')
        consents = None

        if request.GET.get('subject_identifier'):
            consents = consent_model.objects.filter(
                subject_identifier=request.GET.get('subject_identifier'))

        if consents:
            latest_consent = consents.latest('consent_datetime')
            if (self.get_consent_version(latest_consent) == latest_consent.version
                    and request.GET.dict().get('next')):

                url_name = request.GET.dict().get('next').split(',')[0]
                attrs = request.GET.dict().get('next').split(',')[1:]
                options = {k: request.GET.dict().get(k)
                           for k in attrs if request.GET.dict().get(k)}

                url_name = settings.DASHBOARD_URL_NAMES.get(
                    'subject_dashboard_url')
                options['subject_identifier'] = request.GET.get(
                    'subject_identifier')
                del options['screening_identifier']
                try:
                    redirect_url = reverse(url_name, kwargs=options)
                except NoReverseMatch as e:
                    raise ModelAdminNextUrlRedirectError(
                        f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url

    def get_consent_version(self, screening_identifier):

        consent_version_cls = django_apps.get_model(
            'flourish_caregiver.flourishconsentversion')

        try:
            consent_version_obj = consent_version_cls.objects.get(
                screening_identifier=screening_identifier)
        except consent_version_cls.DoesNotExist:
            return None
        else:
            return consent_version_obj.version
