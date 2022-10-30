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
