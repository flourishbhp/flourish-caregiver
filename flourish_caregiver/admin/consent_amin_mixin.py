from django.apps import apps as django_apps
from django.db.models import OuterRef, Subquery


class ConsentMixin:
    consent_cls = django_apps.get_model('flourish_caregiver.caregiverchildconsent')

    def prepare_subject_consent(self, consent):
        child_consent_obj = self.consent_cls.objects.filter(
            subject_identifier=consent if isinstance(
                consent, str) else consent.subject_identifier).latest(
            'consent_datetime')
        return self.prepare_consent_dict(child_consent_obj.__dict__)

    def prepare_consent_dict(self, original_dict):
        exclude_options = ['consent_datetime', 'id', '_state',
                           'created', 'modified', 'user_created',
                           'user_modified', 'version']
        return self.remove_dict_options(original_dict, exclude_options)

    def consents_filtered_by_subject(self, obj, subject_identifier):
        consents = self.consent_cls.objects.filter(
            subject_identifier=subject_identifier).order_by('consent_datetime')
        if obj:
            consents = consents.filter(
                version=getattr(obj, 'version', None))
            subquery = consents.filter(
                subject_identifier=OuterRef('subject_identifier')).order_by(
                '-version').values('version')[:1]
            consents = consents.filter(version=Subquery(subquery))
            consents = set([c.subject_identifier for c in self.get_difference(
                consents, obj)])
        return consents

    def get_difference(self, model_objs, obj=None):
        cc_ids = obj.caregiverchildconsent_set.values_list(
            'subject_identifier', 'version')
        consent_version_obj = self.consent_version_obj(
            obj.screening_identifier)
        child_version = getattr(consent_version_obj, 'child_version', None)
        return [x for x in model_objs if (
            x.subject_identifier, x.version) not in cc_ids or x.version != child_version]

    def remove_dict_options(self, input_dict, options):
        input_dict = dict(input_dict)
        for option in options:
            del input_dict[option]
        return input_dict

    def get_caregiver_child_consents(self, subject_identifier, version=None):
        """ Query for caregiver consent objects related to a specific parent
            `subject_identifier` and optionally by `child_version`.
            @param subject_identifier: child identifier
            @param version: child consent version
            @return: unique filtered child_subject_identifier's
        """
        consents = self.consent_cls.objects.filter(
            subject_consent__subject_identifier=subject_identifier)
        if version:
            consents = consents.filter(version=version)
        return set(consents.values_list('subject_identifier', flat=True))

    def consent_version_obj(self, screening_identifier=None):
        consent_version_cls = django_apps.get_model(
            'flourish_caregiver.flourishconsentversion')
        try:
            consent_version_obj = consent_version_cls.objects.get(
                screening_identifier=screening_identifier)
        except consent_version_cls.DoesNotExist:
            return None
        else:
            return consent_version_obj

    def get_subject_identifier(self, screening_identifier):
        try:
            return self.consent_cls.objects.filter(
                screening_identifier=screening_identifier).latest(
                'consent_datetime').subject_identifier
        except self.consent_cls.DoesNotExist:
            return None
