from django import forms
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
import pytz

from edc_appointment.form_validators import AppointmentFormValidator
from edc_appointment.models import Appointment


class AppointmentForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    """Note, the appointment is only changed, never added,
    through this form.
    """

    form_validator_cls = AppointmentFormValidator

    def clean(self):
        cleaned_data = self.cleaned_data

        if (self.instance.visit_code not in ['1000M', '2000M']
                and cleaned_data.get('appt_datetime')):

            visit_definition = self.instance.visits.get(self.instance.visit_code)

            earliest_appt_date = (self.instance.timepoint_datetime -
                                  visit_definition.rlower).astimezone(
                                      pytz.timezone('Africa/Gaborone'))
            latest_appt_date = (self.instance.timepoint_datetime +
                                visit_definition.rupper).astimezone(
                                      pytz.timezone('Africa/Gaborone'))

            if (cleaned_data.get('appt_datetime') < earliest_appt_date.replace(microsecond=0)
                    or cleaned_data.get('appt_datetime') > latest_appt_date.replace(microsecond=0)):
                raise forms.ValidationError(
                            'The appointment datetime cannot be outside the window period, '
                            'please correct. See earliest, ideal and latest datetimes below.')
        super().clean()

    class Meta:
        model = Appointment
        fields = '__all__'
