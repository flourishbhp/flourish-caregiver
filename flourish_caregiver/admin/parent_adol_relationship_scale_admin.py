from functools import partialmethod

from django.apps import apps as django_apps
from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple, ModelAdminFormAutoNumberMixin, \
    StackedInlineMixin

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import ParentAdolRelationshipScaleForm, ParentAdolRelationshipScaleParentForm
from ..helper_classes.utils import get_child_subject_identifier_by_visit
from ..models import MaternalVisit, ParentAdolRelationshipScale, \
    ParentAdolReloScaleParentModel


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

    twin_sufixes = ['25', '35']
    triplet_sufixes = ['36', '46', '56']

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
                subject_identifier, request=request)
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
                subject_identifier, request=request)
            if not obj:
                extra = len(caregiver_child_consents)
        return extra

    def get_caregiver_child_consents(self, subject_ident, request=None):
        visit_id = request.GET.get('maternal_visit')
        visit = MaternalVisit.objects.get(id=visit_id)
        child_subject_identifier = get_child_subject_identifier_by_visit(visit)
        return self.get_valid_kids(subject_ident, child_subject_identifier)

    def get_valid_kids(self, subject_ident, child_subject_identifier):
        if child_subject_identifier:
            return self.check_sibship(subject_ident, child_subject_identifier)
        return []

    def check_sibship(self, subject_ident, child_subject_identifier):
        suffix = child_subject_identifier.split('-')[-1]
        kids = list(set(self.consent_cls.objects.filter(
            subject_consent__subject_identifier=subject_ident).values_list(
            'subject_identifier', flat=True)))
        if self.determine_sibship(suffix) in ['Twin', 'Triplet']:
            return [kid for kid in kids if
                    self.determine_sibship(kid.split('-')[-1]) in ['Twin', 'Triplet']]
        return [child_subject_identifier]

    def determine_sibship(self, suffix):
        if suffix in self.twin_sufixes:
            return "Twin"
        elif suffix in self.triplet_sufixes:
            return "Triplet"
        return "Neither"


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
