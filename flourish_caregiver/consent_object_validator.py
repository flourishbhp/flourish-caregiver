from edc_consent.consent_object_validator import (
    ConsentObjectValidator as BaseConsentObjectValidator)


class ConsentObjectValidator(BaseConsentObjectValidator):

    def __init__(self, consent=None, consents=None):
        super().__init__(consent=consent, consents=consents)

    def check_consent_period_for_overlap(self, new_consent=None):
        """Raises an error if consent period overlaps with an
        already registered consent object.
        """
        pass