from django.contrib import admin
from edc_senaite_interface.admin import SenaiteResultAdminMixin

from ..admin_site import flourish_caregiver_admin
from ..forms import CaregiverRequisitionResultForm
from ..models import CaregiverRequisitionResult


@admin.register(CaregiverRequisitionResult, site=flourish_caregiver_admin)
class CaregiverRequisitionResultAdmin(SenaiteResultAdminMixin, admin.ModelAdmin):

    form = CaregiverRequisitionResultForm
