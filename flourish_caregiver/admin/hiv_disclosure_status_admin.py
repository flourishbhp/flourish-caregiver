from django.apps import apps as django_apps
from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple

from .modeladmin_mixins import CrfModelAdminMixin
from ..admin_site import flourish_caregiver_admin
from ..forms import HIVDisclosureStatusFormA, HIVDisclosureStatusFormB
from ..forms import HIVDisclosureStatusFormC
from ..models import HIVDisclosureStatusA, HIVDisclosureStatusB
from ..models import HIVDisclosureStatusC


class HIVDisclosureStatusAdminMixin(CrfModelAdminMixin, admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': [
                'maternal_visit',
                'report_datetime',
                'associated_child_identifier',
                'disclosed_status',
                'plan_to_disclose',
                'reason_not_disclosed',
                'reason_not_disclosed_other',
                'disclosure_age',
                'who_disclosed',
                'who_disclosed_other',
                'disclosure_difficulty',
                'child_reaction',
                'child_reaction_other',
                'disclosure_intentional',
                'unintentional_disclosure_reason',
                'unintentional_disclosure_other',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {'disclosed_status': admin.VERTICAL,
                    'reason_not_disclosed': admin.VERTICAL,
                    'who_disclosed': admin.VERTICAL,
                    'disclosure_difficulty': admin.VERTICAL,
                    'child_reaction': admin.VERTICAL,
                    'disclosure_intentional': admin.VERTICAL,
                    'plan_to_disclose': admin.VERTICAL}


    filter_horizontal = ('unintentional_disclosure_reason',)

    def child_gt10(self, request):
        try:
            visit_obj = self.visit_model.objects.get(
                id=request.GET.get('maternal_visit'))
        except self.visit_model.DoesNotExist:
            pass
        else:
            onschedule_model = django_apps.get_model(
                visit_obj.appointment.schedule.onschedule_model)
            try:
                onschedule_obj = onschedule_model.objects.get(
                    subject_identifier=visit_obj.appointment.subject_identifier,
                    schedule_name=visit_obj.appointment.schedule_name)
            except onschedule_model.DoesNotExist:
                pass
            else:
                if 'antenatal' not in onschedule_obj.schedule_name:
                    return onschedule_obj.child_subject_identifier


@admin.register(HIVDisclosureStatusA, site=flourish_caregiver_admin)
class HIVDisclosureStatusAdminA(HIVDisclosureStatusAdminMixin,
                                admin.ModelAdmin):
    form = HIVDisclosureStatusFormA

    def add_view(self, request, form_url='', extra_context=None):
        associated_child_identifier = self.child_gt10(request)

        g = request.GET.copy()
        g.update({
            'associated_child_identifier': associated_child_identifier,
        })

        request.GET = g

        return super().add_view(request, form_url, extra_context)

    def changeform_view(self, request, object_id=None, form_url='',
                        extra_context=None):
        g = request.GET.copy()
        g.update({
            'associated_child_identifier': self.child_gt10(request),
        })
        request.GET = g
        return super().changeform_view(request, object_id, form_url, extra_context)


@admin.register(HIVDisclosureStatusB, site=flourish_caregiver_admin)
class HIVDisclosureStatusAdminB(HIVDisclosureStatusAdminMixin,
                                admin.ModelAdmin):
    form = HIVDisclosureStatusFormB

    def add_view(self, request, form_url='', extra_context=None):
        associated_child_identifier = self.child_gt10(request)

        if associated_child_identifier:
            post_fix = int(associated_child_identifier[-2:])
            associated_child_identifier = associated_child_identifier[:-2] + str(
                post_fix + 10)

        g = request.GET.copy()
        g.update({
            'associated_child_identifier': associated_child_identifier,
        })

        request.GET = g

        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        g = request.GET.copy()
        breakpoint()
        g.update({
            'associated_child_identifier': object_id.associated_child_identifier,
        })

        request.GET = g

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)


@admin.register(HIVDisclosureStatusC, site=flourish_caregiver_admin)
class HIVDisclosureStatusAdminC(HIVDisclosureStatusAdminMixin,
                                admin.ModelAdmin):
    form = HIVDisclosureStatusFormC

    def add_view(self, request, form_url='', extra_context=None):
        associated_child_identifier = self.child_gt10(request)

        if associated_child_identifier:
            post_fix = int(associated_child_identifier[-3:])
            associated_child_identifier = associated_child_identifier[:-3] + str(
                post_fix + 20)

        g = request.GET.copy()
        g.update({
            'associated_child_identifier': associated_child_identifier,
        })

        request.GET = g

        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        g = request.GET.copy()
        g.update({
            'associated_child_identifier': object_id.associated_child_identifier,
        })

        request.GET = g

        return super().change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
