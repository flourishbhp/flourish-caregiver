from edc_identifier.infant_identifier import (
    InfantIdentifier as BaseInfantIdentifier)
from edc_identifier.subject_identifier import SubjectIdentifier as BaseSubjectIdentifier


class SubjectIdentifier(BaseSubjectIdentifier):

    template = '{protocol_number}-0{site_id}{device_id}{sequence}'

    def __init__(self, caregiver_type=None, **kwargs):
        self.caregiver_type = caregiver_type
        super().__init__(**kwargs)

    @property
    def identifier(self):
        """Returns a new and unique identifier and updates
        the IdentifierModel.
        """
        if not self._identifier:
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


class InfantIdentifier(BaseInfantIdentifier):

    def __init__(self, supplied_infant_suffix=None, **kwargs):
        self.supplied_infant_suffix = supplied_infant_suffix
        super().__init__(**kwargs)

    @property
    def infant_suffix(self):
        return self.supplied_infant_suffix


class PreFlourishIdentifier(BaseSubjectIdentifier):

    template = 'PF{protocol_number}-0{site_id}{device_id}{sequence}'
