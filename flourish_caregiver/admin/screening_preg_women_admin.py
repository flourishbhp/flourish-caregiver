from django.apps import apps as django_apps
from django.conf import settings
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_model_admin import audit_fieldset_tuple, ModelAdminNextUrlRedirectError

from ..admin_site import flourish_caregiver_admin
from ..forms import ScreeningPregWomenForm
from ..models import ScreeningPregWomen
from .modeladmin_mixins import ModelAdminMixin


@admin.register(ScreeningPregWomen, site=flourish_caregiver_admin)
class ScreeningPregWomenAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = ScreeningPregWomenForm

    search_fields = ['screening_identifier']

    fieldsets = (
        (None, {
            'fields': ('screening_identifier',
                       'report_datetime',
                       'hiv_testing',
                       'breastfeed_intent',)},
         ),
        audit_fieldset_tuple
    )

    radio_fields = {'hiv_testing': admin.VERTICAL,
                    'breastfeed_intent': admin.VERTICAL, }

    list_display = (
        'screening_identifier', 'report_datetime', 'is_eligible', 'is_consented')

    list_filter = ('report_datetime', 'is_eligible', 'is_consented')

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)

        consent_model = django_apps.get_model('flourish_caregiver.subjectconsent')
        consents = None

        if request.GET.get('subject_identifier'):
            consents = consent_model.objects.filter(
                subject_identifier=request.GET.get('subject_identifier'))

        if consents and request.GET.dict().get('next'):
            url_name = request.GET.dict().get('next').split(',')[0]
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}

            url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')
            options['subject_identifier'] = request.GET.get('subject_identifier')
            del options['screening_identifier']
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url
