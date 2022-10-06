from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin

# from flourish_form_validations.form_validators import TbAdolEligibilityFormValidator
from ..models import TbAdolEligibility, MaternalVisit


class TbAdolScreeningForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    # form_validator_cls = TbStudyEligibilityFormValidator
    visit_model = MaternalVisit

    visit_attr = None

    def clean(self):
        return super().clean()

    class Meta:
        model = TbAdolEligibility
        fields = '__all__'

# ccc = CaregiverChildConsent.objects.all().exclude(
#     cohort__startswith='cohort_a')
#
# cci = ccc.values_list('subject_identifier', flat=True).distinct()
#
# nrm = RequisitionMetadata.objects.filter(
#     subject_identifier__in=cci, entry_status='REQUIRED')
#
# for n in nrm:
#     print(n.subject_identifier, n.visit_code)
#     n.entry_status = 'NOT_REQUIRED'
#     n.save()
