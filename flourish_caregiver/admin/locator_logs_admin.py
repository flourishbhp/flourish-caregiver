from django.conf import settings
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from edc_model_admin import ModelAdminNextUrlRedirectError, audit_fieldset_tuple
from ..admin_site import flourish_caregiver_admin
from ..forms import LocatorLogEntryForm
from ..models import LocatorLogEntry, LocatorLog
from .modeladmin_mixins import ModelAdminMixin


@admin.register(LocatorLogEntry, site=flourish_caregiver_admin)
class LocatorLogEntryAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = LocatorLogEntryForm

    fieldsets = (
        (None, {
            'fields': [
                'locator_log',
                'report_datetime',
                'log_status',
                'comment',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'log_status': admin.VERTICAL}

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['locator_log'].queryset = \
            LocatorLog.objects.filter(id=request.GET.get('locator_log'))
        return super(LocatorLogEntryAdmin, self).render_change_form(
            request, context, *args, **kwargs)

    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.GET.dict().get('next'):
            url_name = settings.DASHBOARD_URL_NAMES.get(
                'maternal_dataset_listboard_url')
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url
