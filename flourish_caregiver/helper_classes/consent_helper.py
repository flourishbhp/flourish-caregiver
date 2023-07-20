from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_consent.exceptions import NotConsentedError
from edc_consent.requires_consent import RequiresConsent
from edc_registration.models import RegisteredSubject
from edc_visit_schedule.site_visit_schedules import site_visit_schedules


class ConsentHelper:

    @property
    def pre_flourish_registered_subject_model_cls(self):
        return django_apps.get_model('pre_flourish.PreFlourishRegisteredSubject')

    @staticmethod
    def validate_pre_flourish_registered_subject(instance):
        try:
            consent_helper.pre_flourish_registered_subject_model_cls.objects.get(
                subject_identifier=instance.subject_identifier,
                consent_datetime__lte=instance.report_datetime)
        except ObjectDoesNotExist:
            raise NotConsentedError(
                f'Subject is not registered. Unable to save '
                f'{instance._meta.label_lower}. '
                f'Got {instance.subject_identifier} on '
                f'{instance.report_datetime}.')

    @staticmethod
    def verify_registered_subject(instance):
        """Raises an error if subject is not registered."""
        if 'P' in instance.subject_identifier:
            consent_helper.validate_pre_flourish_registered_subject(instance)
        else:
            try:
                RegisteredSubject.objects.get(
                    subject_identifier=instance.subject_identifier,
                    consent_datetime__lte=instance.report_datetime)
            except ObjectDoesNotExist:
                raise NotConsentedError(
                    f'Subject is not registered. Unable to save '
                    f'{instance._meta.label_lower}. '
                    f'Got {instance.subject_identifier} on '
                    f'{instance.report_datetime}.')

    @staticmethod
    def get_requires_consent(instance, consent_model, schedule=None):
        """Returns a RequiresConsent object for a given instance."""
        report_datetime = instance.report_datetime
        subject_identifier = instance.subject_identifier
        consent_model = schedule.consent_model if schedule else consent_model
        return RequiresConsent(
            model=instance._meta.label_lower,
            subject_identifier=subject_identifier,
            report_datetime=report_datetime,
            consent_model=consent_model,
            version=instance.consent_version)

    @staticmethod
    def get_visit_schedule(instance):
        """Returns the visit schedule for the of a crf that has a visit attribute."""
        if not hasattr(instance, 'visit'):
            return None
        return site_visit_schedules.get_visit_schedule(
            visit_schedule_name=instance.visit.visit_schedule_name)

    @staticmethod
    def raise_not_consented_error(instance):
        """Raises a NotConsentedError if the subject is not registered."""
        raise NotConsentedError(
            f'Subject is not registered. Unable to save '
            f'{instance._meta.label_lower}. '
            f'Got {instance.subject_identifier} on '
            f'{instance.report_datetime}.')

    @staticmethod
    def screening_preg_exists(child_consent_obj):
        preg_women_screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpregwomen')

        try:
            preg_women_screening_cls.objects.get(
                screening_identifier=child_consent_obj.subject_consent
                .screening_identifier)
        except preg_women_screening_cls.DoesNotExist:
            return False
        else:
            return True


consent_helper = ConsentHelper()
