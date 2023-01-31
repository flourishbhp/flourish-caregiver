from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from edc_base.sites.forms import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
import pytz

from edc_appointment.constants import NEW_APPT, IN_PROGRESS_APPT
from edc_appointment.form_validators import AppointmentFormValidator
from edc_appointment.models import Appointment
from flourish_child.models import ChildAssent

from ..models import CaregiverChildConsent, SubjectConsent, FlourishConsentVersion


class AppointmentForm(SiteModelFormMixin, FormValidatorMixin, AppointmentFormValidator,
                      forms.ModelForm):
    """Note, the appointment is only changed, never added,
    through this form.
    """

    def clean(self):
        super().clean()

        cleaned_data = self.cleaned_data

        if "quart" not in self.instance.schedule_name:
            self._check_child_assent(self.instance.subject_identifier)

        if cleaned_data.get('appt_datetime'):

            visit_definition = self.instance.visits.get(self.instance.visit_code)

            earliest_appt_date = (self.instance.timepoint_datetime -
                                  visit_definition.rlower).astimezone(
                pytz.timezone('Africa/Gaborone'))
            latest_appt_date = (self.instance.timepoint_datetime +
                                visit_definition.rupper).astimezone(
                pytz.timezone('Africa/Gaborone'))

            if self.instance.visit_code_sequence == 0 and self.instance.visit_code != '2200T':
                if (cleaned_data.get('appt_datetime') < earliest_appt_date.replace(
                        microsecond=0)
                        or (self.instance.visit_code not in ['1000M', '2000M']
                            and cleaned_data.get('appt_datetime') > latest_appt_date.replace(
                                    microsecond=0))):
                    raise forms.ValidationError(
                        'The appointment datetime cannot be outside the window period, '
                        'please correct. See earliest, ideal and latest datetimes below.')

    def _check_child_assent(self, subject_identifier):

        consent_version_obj = None
        maternal_consent = None
        child_assents_exists = []

        maternal_consents = SubjectConsent.objects.filter(
            subject_identifier=subject_identifier)

        if maternal_consents:
            maternal_consent = maternal_consents.latest('consent_datetime')

        child_consents = CaregiverChildConsent.objects.filter(
            subject_consent__subject_identifier=subject_identifier,
            is_eligible=True, child_age_at_enrollment__gte=7)

        try:
            consent_version_obj = FlourishConsentVersion.objects.get(
                screening_identifier=maternal_consent.screening_identifier)
        except FlourishConsentVersion.DoesNotExist:
            pass

        if child_consents.exists():

            for child_consent in child_consents:
                exists = ChildAssent.objects.filter(
                    subject_identifier=child_consent.subject_identifier,
                    version=consent_version_obj.child_version).exists()
                child_assents_exists.append(exists)
            child_assents_exists = all(child_assents_exists)
            if not child_assents_exists:
                raise ValidationError('Please fill the child assent(s) form(s) first')

    def validate_appt_new_or_complete(self):
        """
        Validates the caregiver appointment model by overriding existing appointment
        validation functions.
        """
        pass

    def validate_sequence(self):
        """Enforce appointment and visit entry sequence.
        """
        if self.cleaned_data.get('appt_status') == IN_PROGRESS_APPT:
            # visit report sequence
            try:
                self.instance.get_previous_by_appt_datetime(
                    subject_identifier=self.instance.subject_identifier,
                    visit_schedule_name=self.instance.visit_schedule_name).maternalvisit
            except ObjectDoesNotExist:
                last_visit = self.appointment_model_cls.visit_model_cls().objects.filter(
                    appointment__subject_identifier=self.instance.subject_identifier,
                    visit_schedule_name=self.instance.visit_schedule_name,
                    report_datetime__lt=self.instance.appt_datetime
                ).order_by('appointment__appt_datetime').last()

                if last_visit:
                    try:

                        next_visit = last_visit.appointment.get_next_by_appt_datetime(
                            subject_identifier=self.instance.subject_identifier,
                            visit_schedule_name=self.instance.visit_schedule_name)
                    except last_visit.appointment.DoesNotExist:
                        pass
                    else:
                        raise forms.ValidationError(
                            f'A previous visit report is required. Enter the visit report for '
                            f'appointment {next_visit.visit_code} before '
                            'starting with this appointment.')
            except AttributeError:
                pass

            # appointment sequence
            try:
                self.instance.get_previous_by_appt_datetime(
                    subject_identifier=self.instance.subject_identifier,
                    visit_schedule_name=self.instance.visit_schedule_name).maternalvisit
            except ObjectDoesNotExist:
                first_new_appt = self.appointment_model_cls.objects.filter(
                    subject_identifier=self.instance.subject_identifier,
                    visit_schedule_name=self.instance.visit_schedule_name,
                    appt_status=NEW_APPT,
                    appt_datetime__lt=self.instance.appt_datetime
                ).order_by('appt_datetime').first()

                if first_new_appt:
                    raise forms.ValidationError(
                        'A previous appointment requires updating. '
                        f'Update appointment for {first_new_appt.visit_code} first.')
            except AttributeError:
                pass

    class Meta:
        model = Appointment
        fields = '__all__'
