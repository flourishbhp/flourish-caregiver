from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.sites import SiteModelFormMixin
from edc_constants.constants import ALIVE
from edc_constants.constants import OFF_STUDY, DEAD, YES, ON_STUDY, NEW, OTHER
from edc_constants.constants import PARTICIPANT, ALIVE, NO, FAILED_ELIGIBILITY
from edc_form_validators import FormValidatorMixin

from edc_action_item.site_action_items import site_action_items
from edc_visit_tracking.constants import COMPLETED_PROTOCOL_VISIT
from edc_visit_tracking.constants import LOST_VISIT, SCHEDULED, MISSED_VISIT
from edc_visit_tracking.form_validators import VisitFormValidator
from flourish_form_validations.form_validators import \
    FormValidatorMixin as FlourishFormValidatorMixin
from flourish_prn.action_items import CAREGIVEROFF_STUDY_ACTION

from ..models import MaternalVisit, SubjectConsent


class MaternalVisitFormValidator(VisitFormValidator, FlourishFormValidatorMixin):
    consent_version_model = 'flourish_caregiver.flourishconsentversion'

    def clean(self):
        super().clean()

        self.subject_identifier = self.cleaned_data.get(
            'appointment').subject_identifier
        id = None
        if self.instance:
            id = self.instance.id
            if not id:
                self.validate_offstudy_model()

        self.validate_against_consent_datetime(self.cleaned_data.get('report_datetime'))

        self.validate_consent_version_obj()

        self.validate_against_onschedule_datetime()

        self.validate_study_status()

        self.validate_lost_to_fu()

        self.validate_death()

        self.validate_is_present()

        self.validate_last_alive_date(id=id)

        # self.validate_brain_scan()

    def validate_brain_scan(self):
        """
        A validation check was added incase the caregiver is not alive,
        so brain scan is only applicable if the caregiver is alive
        """
        self.applicable(
            ALIVE,
            field='survival_status',
            field_applicable='brain_scan'
        )

    def validate_against_onschedule_datetime(self):

        appointment = self.cleaned_data.get('appointment')
        onschedule_model_cls = appointment.schedule.onschedule_model_cls
        schedule_name = appointment.schedule_name

        try:
            onschedule_obj = onschedule_model_cls.objects.get(
                subject_identifier=self.subject_identifier, schedule_name=schedule_name)
        except onschedule_model_cls.DoesNotExist:
            msg = {'__all__': 'OnSchedule object for this visit does not exist.'}
            self._errors.update(msg)
            raise ValidationError(msg)
        else:
            report_datetime = self.cleaned_data.get('report_datetime')
            onschedule_datetime = onschedule_obj.onschedule_datetime
            if report_datetime < onschedule_datetime:
                msg = {'report_datetime':
                       'Report datetime cannot be before Onschedule datetime.'
                       f'Got Report datetime: {report_datetime}, and Onschedule '
                       f'datetime: {onschedule_datetime}'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_data_collection(self):
        if (self.cleaned_data.get('reason') == SCHEDULED
                and self.cleaned_data.get('study_status') == ON_STUDY
                and self.cleaned_data.get('require_crfs') == NO):
            msg = {'require_crfs': 'This field must be yes if participant'
                                   'is on study and present.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_offstudy_model(self):
        maternal_offstudy_cls = django_apps.get_model('flourish_prn.caregiveroffstudy')
        action_cls = site_action_items.get(
            maternal_offstudy_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                action_type__name=CAREGIVEROFF_STUDY_ACTION,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            try:
                maternal_offstudy_cls.objects.get(
                    subject_identifier=self.subject_identifier)
            except maternal_offstudy_cls.DoesNotExist:
                pass
            else:
                raise forms.ValidationError(
                    'Participant has been taken offstudy. Cannot capture any '
                    'new data.')
        else:
            self.maternal_visit = self.cleaned_data.get('maternal_visit') or None
            if not self.maternal_visit or self.maternal_visit.require_crfs == NO:
                raise forms.ValidationError(
                    'Participant is scheduled to be taken offstudy without '
                    'any new data collection. Cannot capture any new data.')

    def validate_lost_to_fu(self):

        reason = self.cleaned_data.get('reason')

        if (reason == LOST_VISIT and
                self.cleaned_data.get('info_source') == 'other_contact'):
            msg = {'info_source': 'Source of information cannot be other contact with '
                                  'participant if participant has been lost to follow up.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_is_present(self):

        reason = self.cleaned_data.get('reason')

        if (reason == LOST_VISIT and
                self.cleaned_data.get('study_status') != OFF_STUDY):
            msg = {'study_status': 'Participant has been lost to follow up, '
                                   'study status should be off study.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        if (reason == COMPLETED_PROTOCOL_VISIT and
                self.cleaned_data.get('study_status') != OFF_STUDY):
            msg = {'study_status': 'Participant is completing protocol, '
                                   'study status should be off study.'}
            self._errors.update(msg)
            raise ValidationError(msg)

        if self.cleaned_data.get('is_present') == YES:
            if self.cleaned_data.get('info_source') != PARTICIPANT:
                raise forms.ValidationError(
                    {'info_source': 'Source of information must be from '
                                    'participant if participant is present.'})

    def validate_death(self):
        if (self.cleaned_data.get('survival_status') == DEAD
                and self.cleaned_data.get('study_status') != OFF_STUDY):
            msg = {'study_status': 'Participant is deceased, study status '
                                   'should be off study.'}
            self._errors.update(msg)
            raise ValidationError(msg)
        if self.cleaned_data.get('survival_status') != ALIVE:
            if (self.cleaned_data.get('is_present') == YES
                    or self.cleaned_data.get('info_source') == PARTICIPANT):
                msg = {'survival_status': 'Participant cannot be present or '
                                          'source of information if their survival status is not'
                                          'alive.'}
                self._errors.update(msg)
                raise ValidationError(msg)

    def validate_last_alive_date(self, id=None):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""

        latest_consent = self.latest_consent_obj
        last_alive_date = self.cleaned_data.get('last_alive_date')
        if (last_alive_date and not self.instance.pk
                and last_alive_date < latest_consent.consent_datetime.date()):
            msg = {'last_alive_date': 'Date cannot be before consent date'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_reason_and_info_source(self):
        pass

    def validate_study_status(self):
        maternal_offstudy_cls = django_apps.get_model(
            'flourish_prn.caregiveroffstudy')
        action_cls = site_action_items.get(
            maternal_offstudy_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        try:
            action_item = action_item_model_cls.objects.get(
                subject_identifier=self.subject_identifier,
                action_type__name=CAREGIVEROFF_STUDY_ACTION,
                status=NEW)
        except action_item_model_cls.DoesNotExist:
            try:
                maternal_offstudy_cls.objects.get(
                    subject_identifier=self.subject_identifier)
            except maternal_offstudy_cls.DoesNotExist:
                pass
            else:
                if self.cleaned_data.get('study_status') == ON_STUDY:
                    raise forms.ValidationError(
                        {'study_status': 'Participant has been taken offstudy.'
                                         ' Cannot be indicated as on study.'})
        else:
            if (action_item.parent_reference_model_obj
                    and self.cleaned_data.get(
                        'report_datetime') >= action_item.parent_reference_model_obj.report_datetime):
                raise forms.ValidationError(
                    'Participant is scheduled to go offstudy.'
                    ' Cannot edit visit until offstudy form is completed.')

        if (self.cleaned_data.get('reason') == FAILED_ELIGIBILITY
                and self.cleaned_data.get('study_status') == ON_STUDY):
            raise forms.ValidationError(
                {
                    'study_status': 'Participant failed eligibility, they cannot be  indicated '
                                    'as on study.'})

    def validate_required_fields(self):

        self.required_if(
            MISSED_VISIT,
            field='reason',
            field_required='reason_missed')

        self.required_if(
            OTHER,
            field='info_source',
            field_required='info_source_other')

    def validate_against_consent_datetime(self, report_datetime):
        """Returns an instance of the current maternal consent or
        raises an exception if not found."""
        subject_consents = self.subject_consent_cls.objects.filter(
            subject_identifier=self.subject_identifier)
        if not self.instance.pk:
            try:
                subject_consents.latest('consent_datetime')

            except SubjectConsent.DoesNotExist:
                raise forms.ValidationError(
                    'Please complete Caregiver Consent form '
                    f'before proceeding.')
            else:
                if report_datetime and report_datetime < subject_consents.latest(
                        'consent_datetime').consent_datetime:
                    raise forms.ValidationError(
                        "Report datetime cannot be before consent datetime")


class MaternalVisitForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):
    form_validator_cls = MaternalVisitFormValidator

    class Meta:
        model = MaternalVisit
        fields = '__all__'
