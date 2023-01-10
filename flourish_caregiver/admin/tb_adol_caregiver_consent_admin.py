from collections import OrderedDict
from functools import partialmethod

from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_consent.actions import (flag_as_verified_against_paper,
                                 unflag_as_verified_against_paper)
from edc_model_admin import (
    ModelAdminFormAutoNumberMixin, ModelAdminInstitutionMixin,
    audit_fieldset_tuple, audit_fields, ModelAdminNextUrlRedirectMixin,
    ModelAdminNextUrlRedirectError, ModelAdminReplaceLabelTextMixin,
    ModelAdminFormInstructionsMixin, ModelAdminAuditFieldsMixin)
from edc_model_admin import ModelAdminBasicMixin, ModelAdminReadOnlyMixin
from simple_history.admin import SimpleHistoryAdmin

from ..admin_site import flourish_caregiver_admin
from ..forms import TbAdolConsentForm, TbAdolChildConsentForm
from ..models import TbAdolConsent, TbAdolChildConsent, CaregiverChildConsent
from .exportaction_mixin import ExportActionMixin
from .modeladmin_mixins import VersionControlMixin
from edc_model_admin import StackedInlineMixin
from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow

class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormAutoNumberMixin,
                      ModelAdminRevisionMixin, ModelAdminReplaceLabelTextMixin,
                      ModelAdminInstitutionMixin, ModelAdminReadOnlyMixin,
                      VersionControlMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminAuditFieldsMixin, ExportActionMixin):
    list_per_page = 10
    date_hierarchy = 'modified'
    empty_value_display = '-'
    enable_nav_sidebar = False

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

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}

        extra_context['form_version'] = self.get_form_version(request)

        return super().add_view(
            request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):

        extra_context = extra_context or {}

        extra_context['form_version'] = self.get_form_version(request)

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
        
        
class TbAdolChildConsentInline(StackedInlineMixin, ModelAdminFormAutoNumberMixin,
                                  admin.StackedInline):
    model = TbAdolChildConsent
    form = TbAdolChildConsentForm

    extra = 0
    max_num = 3
    
    
    
    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'adol_firstname',
                'adol_lastname',
                'adol_dob',
                'adol_gender'
            ),
        }),)
    
    radio_fields = {
        'adol_gender': admin.VERTICAL,
    }
    
        
    
    def get_formset(self, request, obj, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        
        
        initial = []

        
        subject_identifier = request.GET.get('subject_identifier', None)
        
        if subject_identifier:
        
            children = CaregiverChildConsent.objects.filter(
                subject_identifier__istartswith=subject_identifier,
            )
            
            for child in children:
                
                age = relativedelta(get_utcnow().date(), child.child_dob).years
                
                if 10 <= age <= 17:
                    initial.append({
                        'adol_firstname': child.first_name,
                        'adol_lastname': child.last_name,
                        'adol_gender': child.gender,
                        'adol_dob': child.child_dob,
                        'subject_identifier': child.subject_identifier})
                    
            self.extra = len(initial)
            
        formset = super(TbAdolChildConsentInline, self).get_formset(request, obj, **kwargs)
        formset.__init__ = partialmethod(formset.__init__, initial=initial)
        
        return formset



@admin.register(TbAdolConsent, site=flourish_caregiver_admin)
class TbAdolConsentAdmin(ModelAdminBasicMixin, ModelAdminMixin,
                         SimpleHistoryAdmin, admin.ModelAdmin):

    form = TbAdolConsentForm
    
    inlines = [TbAdolChildConsentInline,]

    fieldsets = (
        (None, {
            'fields': (
                'subject_identifier',
                'first_name',
                'last_name',
                'initials',
                'language',
                'is_literate',
                'witness_name',
                'dob',
                'is_dob_estimated',
                'citizen',
                'identity',
                'identity_type',
                'confirm_identity',
                'tb_blood_test_consent',
                'future_studies_contact',
                'samples_future_studies',
            ),
        }),

        ('Review Questions', {
            'fields': (
                'consent_reviewed',
                'study_questions',
                'assessment_score',
                'consent_signature',
                'consent_copy',
                'consent_datetime',

            ),
        }),
        audit_fieldset_tuple
    )

    radio_fields = {
        'language': admin.VERTICAL,
        'is_literate': admin.VERTICAL,
        'gender': admin.VERTICAL,
        'identity_type': admin.VERTICAL,
        'citizen': admin.VERTICAL,
        'is_dob_estimated': admin.VERTICAL,
        'tb_blood_test_consent': admin.VERTICAL,
        'future_studies_contact': admin.VERTICAL,
        'samples_future_studies': admin.VERTICAL,
        'consent_reviewed': admin.VERTICAL,
        'study_questions': admin.VERTICAL,
        'assessment_score': admin.VERTICAL,
        'consent_signature': admin.VERTICAL,
        'consent_copy': admin.VERTICAL,
    }

    list_display = ('subject_identifier',
                    'verified_by',
                    'is_verified',
                    'is_verified_datetime',
                    'first_name',
                    'initials',
                    'dob',
                    'consent_datetime',
                    'created',
                    'modified',
                    'user_created',
                    'user_modified')

    search_fields = ('subject_identifier', 'dob',)

    def get_actions(self, request):
        super_actions = super().get_actions(request)

        if ('flourish_caregiver.change_tbinformedconsent'
                in request.user.get_group_permissions()):
            consent_actions = [
                flag_as_verified_against_paper,
                unflag_as_verified_against_paper]

            # Add actions from this ModelAdmin.
            actions = (self.get_action(action) for action in consent_actions)
            # get_action might have returned None, so filter any of those out.
            actions = filter(None, actions)

            actions = self._filter_actions_by_permissions(request, actions)
            # Convert the actions into an OrderedDict keyed by name.
            actions = OrderedDict(
                (name, (func, name, desc))
                for func, name, desc in actions
            )

            super_actions.update(actions)

        return super_actions

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj=obj) + audit_fields

    def render_change_form(self, request, context, add=False, change=False, form_url='',
                           obj=None):
        context.update({
            'show_save': True,
            'show_save_and_continue': False,
            'show_save_and_add_another': False,
            'show_delete': True
        })
        return super().render_change_form(request, context, add, change, form_url, obj)
