from functools import partialmethod

from django.apps import apps as django_apps
from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple, ModelAdminFormAutoNumberMixin, \
    StackedInlineMixin

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import ParentAdolRelationshipScaleForm, ParentAdolRelationshipScaleParentForm
from ..models import ParentAdolRelationshipScale, ParentAdolReloScaleParentModel


class ParentAdolRelationshipScaleAdmin(StackedInlineMixin,
                                       ModelAdminFormAutoNumberMixin,
                                       admin.StackedInline):
    form = ParentAdolRelationshipScaleForm
    model = ParentAdolRelationshipScale
    extra = 0
    max_num = 3

    consent_cls = django_apps.get_model(
        'flourish_caregiver.caregiverchildconsent')

    readonly_fields = ('shared_activities',
                       'connectedness',
                       'hostility',)

    fieldsets = (
        (
            'Please read each statement below and rate from 0 (Not At All True) to 5 '
            '(Nearly Always or Always True) how true the statements typically are of '
            'your relationship with your adolescent. There are no right or wrong '
            'answers. Do not spend too much time on any statement. ',
            {
                'fields': [
                    'associated_child_identifier',
                    'eat_together',
                    'time_together',
                    'family_events_together',
                    'support_from_others',
                    'show_affection',
                    'comfort',
                    'negative_comments',
                    'compassion',
                    'upset',
                    'play_sport',
                    'complains_about_me',
                    'encourage',
                    'criticize_child',
                    'change_attitude',
                    'encourage_expression',
                    'shared_activities',
                    'connectedness',
                    'hostility',
                ]}
        ),)

    radio_fields = {
        'eat_together': admin.HORIZONTAL,
        'time_together': admin.HORIZONTAL,
        'family_events_together': admin.HORIZONTAL,
        'support_from_others': admin.HORIZONTAL,
        'show_affection': admin.HORIZONTAL,
        'comfort': admin.HORIZONTAL,
        'negative_comments': admin.HORIZONTAL,
        'compassion': admin.HORIZONTAL,
        'upset': admin.HORIZONTAL,
        'play_sport': admin.HORIZONTAL,
        'complains_about_me': admin.HORIZONTAL,
        'encourage': admin.HORIZONTAL,
        'criticize_child': admin.HORIZONTAL,
        'change_attitude': admin.HORIZONTAL,
        'encourage_expression': admin.HORIZONTAL
    }

    def get_formset(self, request, obj=None, **kwargs):
        subject_identifier = request.GET.get('subject_identifier')
        initial = []
        if subject_identifier:
            caregiver_child_consents = self.get_caregiver_child_consents(
                subject_identifier)
            for child_identifier in caregiver_child_consents:
                initial.append({'associated_child_identifier': child_identifier})
        formset = super().get_formset(request, obj=obj, **kwargs)
        formset.form = self.auto_number(formset.form)
        formset.__init__ = partialmethod(formset.__init__, initial=initial)
        return formset

    def get_extra(self, request, obj=None, **kwargs):
        extra = super().get_extra(request, obj, **kwargs)
        subject_identifier = request.GET.get('subject_identifier')
        if subject_identifier:
            caregiver_child_consents = self.get_caregiver_child_consents(
                subject_identifier)
            if not obj:
                extra = len(caregiver_child_consents)
        return extra

    def get_caregiver_child_consents(self, subject_ident):
        return set(list(self.consent_cls.objects.filter(
            subject_consent__subject_identifier=subject_ident
        ).values_list('subject_identifier', flat=True)))


@admin.register(ParentAdolReloScaleParentModel, site=flourish_caregiver_admin)
class ParentAdolRelationshipScaleParentAdmin(CrfModelAdminMixin, admin.ModelAdmin):
    form = ParentAdolRelationshipScaleParentForm
    inlines = [ParentAdolRelationshipScaleAdmin, ]

    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
            ]}
         ), audit_fieldset_tuple)
