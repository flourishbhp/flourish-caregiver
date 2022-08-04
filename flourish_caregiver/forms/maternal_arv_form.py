from django import forms
from edc_constants.constants import NO, YES

from flourish_form_validations.form_validators.maternal_arv_at_delivery_form_validations import \
    MaternalArvAtDeliveryFormValidations
from .form_mixins import InlineSubjectModelFormMixin, SubjectModelFormMixin
from ..models import MaternalArvAtDelivery, MaternalArvTableAtDelivery


class MaternalArvAtDeliveryForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = MaternalArvAtDeliveryFormValidations

    def clean(self):
        cleaned_data = super().clean()

        maternal_arv_count = self.data.get(
            'maternalarvtableatdelivery_set-TOTAL_FORMS')

        if int(maternal_arv_count) == 0 and cleaned_data.get('last_visit_change') != YES:
            raise forms.ValidationError('Please complete the maternal arv table.')

        elif int(maternal_arv_count) != 0 and cleaned_data.get('last_visit_change') == NO:
            raise forms.ValidationError('Maternal ARV tables are not required.')

        self.validate_date_resumed()

    def validate_date_resumed(self):
        maternal_arv_count = self.data.get(
            'maternalarvtableatdelivery_set-TOTAL_FORMS')

        if int(maternal_arv_count) != 0 and self.cleaned_data.get('resume_treat') == YES:
            for i in range(int(maternal_arv_count)):
                maternal_arv_date_resumed = self.data.get(
                    'maternalarvtableatdelivery_set-' + str(i) + '-date_resumed')
                breakpoint()
                if maternal_arv_date_resumed == "":
                    raise forms.ValidationError('Maternal ARV tables date resumed '
                                                'is required')
        elif self.cleaned_data.get('resume_treat') == YES:
            raise forms.ValidationError('Please complete the maternal arv table.')


    class Meta:
        model = MaternalArvAtDelivery
        fields = '__all__'


class MaternalArvTableAtDeliveryForm(InlineSubjectModelFormMixin):
    class Meta:
        model = MaternalArvTableAtDelivery
        fields = '__all__'
