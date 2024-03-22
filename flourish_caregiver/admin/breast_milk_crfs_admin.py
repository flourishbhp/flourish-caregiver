from django.contrib import admin
from edc_fieldsets import Remove
from edc_model_admin import audit_fieldset_tuple, StackedInlineMixin

from flourish_caregiver.admin.modeladmin_mixins import CrfModelAdminMixin
from flourish_caregiver.admin_site import flourish_caregiver_admin
from flourish_caregiver.forms import BreastMilk6MonthsForms, BreastMilkBirthForms, \
    CrackedNipplesInlineForm, MastitisInlineForm
from flourish_caregiver.models import BreastMilk6Months, BreastMilkBirth
from flourish_caregiver.models.breast_milk_crfs import CrackedNipplesInline, \
    MastitisInline


class MastitisInlineAdmin(StackedInlineMixin, admin.StackedInline):
    model = MastitisInline
    form = MastitisInlineForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': [
                'mastitis_date_onset',
                'mastitis_type',
                'mastitis_action',
                'mastitis_action_other']}
         ),)

    radio_fields = {
        'mastitis_type': admin.VERTICAL,
    }

    filter_horizontal = ('mastitis_action',)


class CrackedNipplesInlineAdmin(StackedInlineMixin, admin.StackedInline):
    model = CrackedNipplesInline
    form = CrackedNipplesInlineForm
    extra = 0

    fieldsets = (
        (None, {
            'fields': (
                'cracked_nipples_date_onset',
                'cracked_nipples_type',
                'cracked_nipples_action',
                'cracked_nipples_action_other')}
         ),)

    radio_fields = {
        'cracked_nipples_type': admin.VERTICAL,
    }

    filter_horizontal = ('cracked_nipples_action',)


class BreastMilkAdminMixin(CrfModelAdminMixin, admin.ModelAdmin):
    inlines = [MastitisInlineAdmin, CrackedNipplesInlineAdmin]

    fieldsets = (
        (None, {
            'fields': (
                'maternal_visit',
                'report_datetime',
                'exp_mastitis',
                'exp_mastitis_count',
                'exp_cracked_nipples',
                'exp_cracked_nipples_count',
                'milk_collected',
                'not_collected_reasons',
                'recently_ate',
                'breast_collected',
                'milk_collected_volume',
                'last_breastfed',
                'add_comments',

            )}
         ), audit_fieldset_tuple)

    radio_fields = {
        'exp_mastitis': admin.VERTICAL,
        'exp_mastitis_count': admin.VERTICAL,
        'exp_cracked_nipples': admin.VERTICAL,
        'exp_cracked_nipples_count': admin.VERTICAL,
        'recently_ate': admin.VERTICAL,
        'milk_collected': admin.VERTICAL,
        'not_collected_reasons': admin.VERTICAL,
        'breast_collected': admin.VERTICAL,
    }

    search_fields = 'maternal_visit__subject_identifier',

    conditional_fieldlists = {
        '2002S': Remove('recently_ate')
    }

    def get_key(self, request, obj=None):
        model_obj = self.get_instance(request)
        return getattr(model_obj, 'visit_code', None)


@admin.register(BreastMilkBirth, site=flourish_caregiver_admin)
class BreastMilkBirthAdmin(BreastMilkAdminMixin, admin.ModelAdmin):
    form = BreastMilkBirthForms


@admin.register(BreastMilk6Months, site=flourish_caregiver_admin)
class BreastMilk6MonthsAdmin(BreastMilkAdminMixin, admin.ModelAdmin):
    form = BreastMilk6MonthsForms
