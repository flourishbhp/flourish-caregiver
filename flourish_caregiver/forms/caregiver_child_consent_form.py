from django.core.exceptions import ValidationError

from edc_constants.choices import FEMALE, MALE

from ..models import CaregiverChildConsent
from .form_mixins import SubjectModelFormMixin


class CaregiverChildConsentForm(SubjectModelFormMixin):

    def clean(self):
        super().clean()

        self.validate_identity_number(cleaned_data=self.cleaned_data)

    def validate_identity_number(self, cleaned_data=None):
        if cleaned_data.get('identity') != cleaned_data.get(
                'confirm_identity'):
            msg = {'identity':
                       '\'Identity\' must match \'confirm identity\'.'}
            self._errors.update(msg)
            raise ValidationError(msg)
        if cleaned_data.get('identity_type') == 'country_id':
            if len(cleaned_data.get('identity')) != 9:
                msg = {'identity':
                           'Country identity provided should contain 9 values. '
                           'Please correct.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            gender = cleaned_data.get('gender')
            if gender == FEMALE and cleaned_data.get('identity')[4] != '2':
                msg = {'identity':
                           'Participant gender is Female. Please correct identity number.'}
                self._errors.update(msg)
                raise ValidationError(msg)
            elif gender == MALE and cleaned_data.get('identity')[4] != '1':
                msg = {'identity':
                           'Participant is Male. Please correct identity number.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    class Meta:
        model = CaregiverChildConsent
        fields = '__all__'
