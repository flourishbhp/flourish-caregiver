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
            screening_identifiers = [subject_screening_obj, ]

        if screening_identifiers:

            try:
                consent_version_obj = consent_version_cls.objects.get(
                    screening_identifier__in=screening_identifiers)
            except consent_version_cls.DoesNotExist:
                raise ValidationError(
                    'Missing Consent Version form. Please complete '
                    'it before proceeding.')
            return consent_version_obj.version

    def save(self, *args, **kwargs):
        self.consent_version = self.get_consent_version()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
