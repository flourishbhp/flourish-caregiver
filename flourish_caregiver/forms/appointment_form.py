from django import forms
from django.core.exceptions import ValidationError
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
import pytz

from edc_appointment.form_validators import AppointmentFormValidator
from edc_appointment.models import Appointment
from flourish_caregiver.models.caregiver_child_consent import CaregiverChildConsent
from flourish_child.models import ChildAssent


class AppointmentForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    """Note, the appointment is only changed, never added,
    through this form.
    """

    form_validator_cls = AppointmentFormValidator

    def clean(self):
        cleaned_data = self.cleaned_data

        self._check_child_assent(self.instance.subject_identifier)

        if cleaned_data.get('appt_datetime'):

            visit_definition = self.instance.visits.get(self.instance.visit_code)

            earliest_appt_date = (self.instance.timepoint_datetime -
                                  visit_definition.rlower).astimezone(
                pytz.timezone('Africa/Gaborone'))
            latest_appt_date = (self.instance.timepoint_datetime +
                                visit_definition.rupper).astimezone(
                pytz.timezone('Africa/Gaborone'))

            if (cleaned_data.get('appt_datetime') < earliest_appt_date.replace(microsecond=0)
                    or (self.instance.visit_code not in ['1000M', '2000M']
                        and cleaned_data.get('appt_datetime') > latest_appt_date.replace(
                            microsecond=0))):
                raise forms.ValidationError(
                    'The appointment datetime cannot be outside the window period, '
                    'please correct. See earliest, ideal and latest datetimes below.')

        super().clean()

    def _check_child_assent(self, subject_identifier):

        child_assents_exists = []

        child_consents = CaregiverChildConsent.objects.filter(
            subject_consent__subject_identifier=subject_identifier,
            is_eligible=True, child_age_at_enrollment__gte=7)

        if child_consents.exists():

            for child_consent in child_consents:
                exists = ChildAssent.objects.filter(
                    subject_identifier=child_consent.subject_identifier,
                    version=child_consent.version).exists()
                child_assents_exists.append(exists)

            child_assents_exists = all(child_assents_exists)

            if not child_assents_exists:
                raise ValidationError('Please fill the child assent(s) form(s) first')

    class Meta:
        model = Appointment
        fields = '__all__'
