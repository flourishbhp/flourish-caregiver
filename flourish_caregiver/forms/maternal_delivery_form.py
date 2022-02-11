from dateutil.relativedelta import relativedelta
from django import forms
from django.core.exceptions import ValidationError
from edc_base.sites import SiteModelFormMixin
from edc_constants.constants import POS, YES, NOT_APPLICABLE
from edc_form_validators import FormValidatorMixin

from flourish_form_validations.form_validators import MaternalDeliveryFormValidator
from ..helper_classes import MaternalStatusHelper
from ..models import MaternalDelivery


class MaternalDeliveryForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = MaternalDeliveryFormValidator

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def validate_valid_regime_hiv_pos_only(self, cleaned_data=None):
        if self.maternal_status_helper.hiv_status == POS:
            if cleaned_data.get('valid_regiment_duration') != YES:
                message = {'valid_regiment_duration':
                               'Participant is HIV+ valid regimen duration '
                               'should be YES. Please correct.'}
                self._errors.update(message)
                raise ValidationError(message)
            self.required_if(
                YES,
                field='valid_regiment_duration',
                field_required='arv_initiation_date',
                required_msg='You indicated participant was on valid regimen, '
                             'please give a valid arv initiation date.'
            )
            if (cleaned_data.get('valid_regiment_duration') == YES and
                    (cleaned_data.get('delivery_datetime').date() - relativedelta(
                        weeks=4) <
                     cleaned_data.get('arv_initiation_date'))):
                message = {'delivery_datetime':
                               'You indicated that the mother was on REGIMEN for a '
                               'valid duration, but delivery date is within 4weeks '
                               'of art initiation date. Please correct.'}
                self._errors.update(message)
                raise ValidationError(message)
        else:
            status = self.maternal_status_helper.hiv_status
            if cleaned_data.get('valid_regiment_duration') not in [NOT_APPLICABLE]:
                message = {'valid_regiment_duration':
                               f'Participant\'s HIV status is {status}, '
                               'valid regimen duration should be Not Applicable.'}
                self._errors.update(message)
                raise ValidationError(message)

            if cleaned_data.get('arv_initiation_date'):
                message = {'arv_initiation_date':
                               f'Participant\'s HIV status is {status}, '
                               'arv initiation date should not filled.'}
                self._errors.update(message)
                raise ValidationError(message)

    @property
    def maternal_status_helper(self):
        cleaned_data = self.cleaned_data
        latest_visit = self.maternal_visit_cls.objects.filter(
            subject_identifier=cleaned_data.get(
                'subject_identifier')).order_by('-created').first()
        if latest_visit:
            return MaternalStatusHelper(latest_visit)
        else:
            raise ValidationError(
                'Please complete previous visits before filling in '
                'Maternal Labour Delivery Form.')

    class Meta:
        model = MaternalDelivery
        fields = '__all__'
