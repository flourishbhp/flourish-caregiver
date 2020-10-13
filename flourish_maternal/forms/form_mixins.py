from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_visit_tracking.crf_date_validator import CrfDateValidator
from edc_visit_tracking.crf_date_validator import (
    CrfReportDateAllowanceError, CrfReportDateBeforeStudyStart)
from edc_visit_tracking.crf_date_validator import CrfReportDateIsFuture

from ..models import MaternalVisit


class SubjectModelFormMixin(SiteModelFormMixin, FormValidatorMixin,
                            forms.ModelForm):

    visit_model = MaternalVisit

    visit_attr = None

    def clean(self):
        visit_codes = ['1000M', '1010M', '1020M']
        cleaned_data = super().clean()
        if (cleaned_data.get('maternal_visit')
                and cleaned_data.get('maternal_visit').visit_code
                not in visit_codes):
            if cleaned_data.get('report_datetime'):
                try:
                    CrfDateValidator(
                        report_datetime=cleaned_data.get('report_datetime'),
                        visit_report_datetime=cleaned_data.get(
                            self._meta.model.visit_model_attr()).report_datetime)
                except (CrfReportDateAllowanceError, CrfReportDateBeforeStudyStart,
                        CrfReportDateIsFuture) as e:
                    raise forms.ValidationError(e)
        return cleaned_data
