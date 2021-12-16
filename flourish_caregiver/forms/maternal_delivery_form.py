from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from flourish_form_validations.form_validators import MaternalDeliveryFormValidator
from ..models import ArvsPrePregnancy
from ..models import MaternalDelivery


class MaternalDeliveryForm(
    SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = MaternalDeliveryFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def __init__(self, *args, **kwargs):
        super(MaternalDeliveryForm, self).__init__(*args, **kwargs)

        subject_identifier = self.initial.get('subject_identifier', None)

        try:
            pre_pregnancy = ArvsPrePregnancy.objects.get(
                maternal_visit__appointment__subject_identifier=subject_identifier)
        except ArvsPrePregnancy.DoesNotExist:
            pass
        else:
            self.fields['arv_initiation_date'].widget = forms.TextInput(attrs={'readonly': 'readonly'}, )
            self.initial['arv_initiation_date'] = pre_pregnancy.art_start_date

    class Meta:
        model = MaternalDelivery
        fields = '__all__'
