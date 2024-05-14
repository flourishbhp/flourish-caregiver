import re
from edc_identifier.infant_identifier import (
    InfantIdentifier as BaseInfantIdentifier)
from edc_identifier.subject_identifier import SubjectIdentifier as BaseSubjectIdentifier


class SubjectIdentifier(BaseSubjectIdentifier):

    template = '{protocol_number}-0{site_id}{device_id}{sequence}'

    def __init__(self, caregiver_type=None, pf_identifier=None, **kwargs):
        self.caregiver_type = caregiver_type
        self.pf_identifier = pf_identifier
        super().__init__(**kwargs)

    @property
    def identifier(self):
        """Returns a new and unique identifier and updates
        the IdentifierModel.
        """
        if not self._identifier:
            if self.pf_identifier:
                self.reuse_pre_flourish_identifier()

            if not self.pf_identifier:
                self.pre_identifier()
                self._identifier = self.template.format(**self.template_opts)
                check_digit = self.checkdigit.calculate_checkdigit(
                    ''.join(self._identifier.split('-')))
                if self.caregiver_type:
                    self._identifier = f'{self.caregiver_type}{self._identifier}-{check_digit}'
                self.identifier_model = self.identifier_model_cls.objects.create(
                    name=self.label,
                    sequence_number=self.sequence_number,
                    identifier=self._identifier,
                    protocol_number=self.protocol_number,
                    device_id=self.device_id,
                    model=self.requesting_model,
                    site=self.site,
                    identifier_type=self.identifier_type)
                self.post_identifier()
        return self._identifier

    def reuse_pre_flourish_identifier(self):
        """ For participant enrolling from pre-flourish try:
            reuse identifier from pre-flourish or generate a new identifier
            for them.
        """
        pattern = r'(\w)(\d{3})-0(\d{2})(\d{2})(\d{4})-(\d)'
        re_match = re.match(pattern, self.pf_identifier)
        sequence = re_match.group(5)
        if self.caregiver_type:
            self.pf_identifier = self.pf_identifier.replace(
                re_match.group(1), self.caregiver_type)

        try:
            self.identifier_model_cls.objects.get(
                identifier=self.pf_identifier)
        except self.identifier_model_cls.DoesNotExist:
            self.pre_identifier()
            self.identifier_model = self.identifier_model_cls.objects.create(
                name=self.label,
                sequence_number=sequence,
                identifier=self.pf_identifier,
                protocol_number=self.protocol_number,
                device_id=self.device_id,
                model=self.requesting_model,
                site=self.site,
                identifier_type=self.identifier_type)
            self._identifier = self.pf_identifier
            self.post_identifier()
        else:
            self.pf_identifier = None


class InfantIdentifier(BaseInfantIdentifier):

    def __init__(self, supplied_infant_suffix=None, **kwargs):
        self.supplied_infant_suffix = supplied_infant_suffix
        super().__init__(**kwargs)

    @property
    def infant_suffix(self):
        return self.supplied_infant_suffix


class PreFlourishIdentifier(BaseSubjectIdentifier):

    template = 'PF{protocol_number}-0{site_id}{device_id}{sequence}'
