from edc_constants.constants import NO, UNKNOWN

from ..constants import (MAX_AGE_OF_CONSENT, MIN_AGE_OF_CONSENT)


class AntenatalEnrollmentEligibility:

    def __init__(self, is_diabetic=None, will_breastfeed=None,
                 will_remain_onstudy=None):
        self.is_diabetic = is_diabetic
        self.will_breastfeed = will_breastfeed
        self.reasons = []
        self.will_remain_onstudy = will_remain_onstudy
        self.eligible = None
        if not self.is_diabetic and self.will_breastfeed \
                and self.will_remain_onstudy:
            self.eligible = True
        if self.is_diabetic:
            self.reasons.append('Participant is diabetic')
        if not self.will_breastfeed:
            self.reasons.append(
                'Participant is not willing to breastfeed')
        if not self.will_remain_onstudy:
            self.reasons.append(
                'Participant is not willing to remain on study')


class BHPPriorEligibilty:
    def __init__(self, child_alive=None, flourish_interest=None,
                 flourish_participation=None, **kwargs):
        """checks if prior BHP participants are eligible otherwise
            error message is the reason for eligibility test failed."""
        self.error_message = []
        self.child_alive = child_alive
        self.flourish_interest = flourish_interest
        self.flourish_participation = flourish_participation
        if self.child_alive in [NO, UNKNOWN]:
            self.error_message.append(
                'The child from the previous study is not alive.')
        if self.flourish_interest == NO:
            self.error_message.append(
                'Child caregiver not interested in learning about flourish.')
        if self.flourish_participation == NO:
            self.error_message.append(
                'Not interested in participating in the Flourish study.')
        self.is_eligible = False if self.error_message else True


class Eligibility:

    def __init__(self, age_in_years=None, has_omang=None, **kwargs):
        """checks if mother is eligible otherwise'
        ' error message is the reason for'
        ' eligibility test failed."""
        self.error_message = []
        self.age_in_years = age_in_years
        self.has_omang = has_omang
        if self.age_in_years < MIN_AGE_OF_CONSENT:
            self.error_message.append(
                'Mother is under {}'.format(MIN_AGE_OF_CONSENT))
        if self.age_in_years > MAX_AGE_OF_CONSENT:
            self.error_message.append(
                'Mother is too old (>{})'.format(MAX_AGE_OF_CONSENT))
        if self.has_omang == NO:
            self.error_message.append('Not a citizen')
        self.is_eligible = False if self.error_message else True

    def __str__(self):
        return "Screened, age ({})".format(self.age_in_years)
