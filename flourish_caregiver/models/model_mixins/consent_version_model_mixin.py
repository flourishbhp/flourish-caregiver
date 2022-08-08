from django.apps import apps as django_apps
from django.core.exceptions import ValidationError


class ConsentVersionModelModelMixin:

    """ Base model for all models
    """

    def get_consent_version(self):
        preg_subject_screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpregwomen')
        prior_subject_screening_cls = django_apps.get_model(
            'flourish_caregiver.screeningpriorbhpparticipants')

        consent_version_cls = django_apps.get_model(
            'flourish_caregiver.flourishconsentversion')

        subject_screening_obj = None

        try:
            subject_screening_obj = preg_subject_screening_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except preg_subject_screening_cls.DoesNotExist:

            subject_screening_objs = prior_subject_screening_cls.objects.filter(
                    subject_identifier=self.subject_identifier)

            if not subject_screening_objs:
                raise ValidationError(
                    'Missing Subject Screening form. Please complete '
                    'it before proceeding.')

        if subject_screening_objs:
            screening_identifiers = subject_screening_objs.values_list(
                'screening_identifier', flat=True)
        elif subject_screening_obj:
            screening_identifiers = [subject_screening_obj.screening_identifier, ]

        if screening_identifiers:

            consent_version_obj = consent_version_cls.objects.filter(
                    screening_identifier__in=screening_identifiers)

            if consent_version_obj.count() > 1:
                raise ValidationError(
                    'Multiple Consent Version forms found. Please correct '
                    'before proceeding.')
            elif not consent_version_obj:
                raise ValidationError(
                    'Missing Consent Version form. Please complete '
                    'it before proceeding.')
            else:
                return consent_version_obj[0].version

    def save(self, *args, **kwargs):
        self.consent_version = self.get_consent_version()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
