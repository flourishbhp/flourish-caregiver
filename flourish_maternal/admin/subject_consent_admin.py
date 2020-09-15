from collections import OrderedDict

from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_consent.actions import (
    flag_as_verified_against_paper, unflag_as_verified_against_paper)
from edc_model_admin import (
    ModelAdminFormAutoNumberMixin, ModelAdminInstitutionMixin,
    audit_fieldset_tuple, audit_fields, ModelAdminNextUrlRedirectMixin,
    ModelAdminNextUrlRedirectError, ModelAdminReplaceLabelTextMixin)
from edc_model_admin import ModelAdminBasicMixin, ModelAdminReadOnlyMixin
from simple_history.admin import SimpleHistoryAdmin

from ..admin_site import flourish_maternal_admin
from ..forms import SubjectConsentForm
from ..models import SubjectConsent


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminReplaceLabelTextMixin,
                      ModelAdminInstitutionMixin, ModelAdminReadOnlyMixin):

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


@admin.register(SubjectConsent, site=flourish_maternal_admin)
class SubjectConsentAdmin(ModelAdminBasicMixin, ModelAdminMixin,
                          SimpleHistoryAdmin,
                          admin.ModelAdmin):

    form = SubjectConsentForm

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'screening_identifier',
                'identity_type',
                'recruit_source',
                'recruit_source_other',
                'recruitment_clinic',
                'recruitment_clinic_other',)}),
        audit_fieldset_tuple)

    radio_fields = {
        "identity_type": admin.VERTICAL,
        "recruit_source": admin.VERTICAL,
        "recruitment_clinic": admin.VERTICAL,
    }

    def get_readonly_fields(self, request, obj=None):
        return (super().get_readonly_fields(request, obj=obj)
                + audit_fields)

