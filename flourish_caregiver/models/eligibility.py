from edc_constants.constants import NO, UNKNOWN


class AntenatalEnrollmentEligibility:

    def __init__(self, will_breastfeed=None):
        self.will_breastfeed = will_breastfeed
        self.reasons = []
        self.eligible = None
        if self.will_breastfeed:
            self.eligible = True
        if not self.will_breastfeed:
            self.reasons.append(
                'Participant is not willing to breastfeed')


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


class PregWomenEligibility:

    def __init__(self, hiv_testing=None, breastfeed_intent=None, **kwargs):
        """checks if pregnant women enrolling is eligible otherwise'
        ' error message is the reason for'
        ' eligibility test failed."""
        self.error_message = []
        self.hiv_testing = hiv_testing
        self.breastfeed_intent = breastfeed_intent
        if self.hiv_testing == NO:
            self.error_message.append(
                'Participant is not willing to undergo HIV testing and counseling.')
        if self.breastfeed_intent == NO:
            self.error_message.append(
                'Participant does not intend on breastfeeding.')
        self.is_eligible = False if self.error_message else True
