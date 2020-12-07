from django.contrib import admin
from edc_model_admin import audit_fieldset_tuple
from ..admin_site import flourish_caregiver_admin
from ..forms import LocatorLogForm
from ..models import LocatorLog, MaternalDataset
from .modeladmin_mixins import ModelAdminMixin


@admin.register(LocatorLog, site=flourish_caregiver_admin)
class LocatorLogAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = LocatorLogForm

    fieldsets = (
        (None, {
            'fields': [
                'maternal_dataset',
                'report_datetime',
                'log_status',
                'comment',
            ]}
         ), audit_fieldset_tuple)

    radio_fields = {
        'log_status': admin.VERTICAL}

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['maternal_dataset'].queryset = \
            MaternalDataset.objects.filter(id=request.GET.get('maternal_dataset'))
        return super(LocatorLogAdmin, self).render_change_form(
            request, context, *args, **kwargs)
