from edc_constants.constants import NO, UNKNOWN, POS


class AntenatalEnrollmentEligibility:

    def __init__(self, will_breastfeed=None, ga_lmp_enrollment_wks=None,
                 enrollment_hiv_status=None, will_get_arvs=None,
                 pending_ultrasound=None, rapid_test_done=None):

        self.error_message = []
        self.is_eligible = True

        if pending_ultrasound:
            self.is_eligible = False
            self.error_message.append('Pending ultrasound.')
        else:
            lmp_to_use = ga_lmp_enrollment_wks
            if lmp_to_use < 22 or lmp_to_use > 28:
                self.error_message.append('Gestation not 22 to 28wks.')
                self.is_eligible = False
            if will_breastfeed == NO:
                self.error_message.append('Will not breastfeed.')
                self.is_eligible = False
            if enrollment_hiv_status == POS and will_get_arvs == NO:
                self.error_message.append('Will not get ARVs on this pregnancy.')
                self.is_eligible = False
            if rapid_test_done == NO:
                self.error_message.append('Rapid test not done.')
                self.is_eligible = False


class BHPPriorEligibilty:

    def __init__(self, child_alive=None, mother_alive=None,
                 flourish_interest=None, flourish_participation=None):
        """checks if prior BHP participants are eligible otherwise
            error message is the reason for eligibility test failed."""
        self.error_message = []
        self.child_alive = child_alive
        self.mother_alive = mother_alive
        self.flourish_interest = flourish_interest
        self.flourish_participation = flourish_participation
        if self.child_alive in [NO, UNKNOWN]:
            self.error_message.append(
                'The child from the previous study is not alive.')
        if self.mother_alive in [NO, UNKNOWN] and self.flourish_interest == NO:
            self.error_message.append(
                'Child caregiver not interested in learning about flourish.')
        if self.flourish_participation in [NO, 'undecided']:
            self.error_message.append(
                'Not interested in participating in the Flourish study.')
        self.is_eligible = False if self.error_message else True


class PregWomenEligibility:

    def __init__(self, hiv_testing=None, breastfeed_intent=None):
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


class ConsentEligibility:

    def __init__(self, remain_in_study=None, hiv_testing=None, breastfeed_intent=None,
                 consent_reviewed=None, citizen=None, study_questions=None,
                 assessment_score=None, consent_signature=None, consent_copy=None,
                 child_consent=None):
        self.error_message = []
        self.remain_in_study = remain_in_study
        self.hiv_testing = hiv_testing
        self.breastfeed_intent = breastfeed_intent
        self.consent_reviewed = consent_reviewed
        self.study_questions = study_questions
        self.assessment_score = assessment_score
        self.consent_signature = consent_signature
        self.consent_copy = consent_copy
        self.child_consent = child_consent
        if self.remain_in_study == NO:
            self.error_message.append(
                'Participant is not willing to remain in study area until 2025.')
        if self.hiv_testing == NO:
            self.error_message.append(
                'Participant is not willing to undergo HIV testing and counseling.')
        if self.breastfeed_intent == NO:
            self.error_message.append(
                'Participant does not intend on breastfeeding.')
        if self.consent_reviewed == NO:
            self.error_message.append(
                'Consent was not reviewed with the participant.')
        if self.study_questions == NO:
            self.error_message.append(
                'Did not answer all questions the participant had about the study.')
        if self.assessment_score == NO:
            self.error_message.append(
                'Participant did not demonstrate understanding of the study.')
        if self.consent_signature == NO:
            self.error_message.append(
                'Participant did not sign the consent form.')
        if self.consent_copy == NO:
            self.error_message.append(
                'Participant was not provided with a copy of their informed consent.')
        if self.child_consent == NO:
            self.error_message.append(
                'Participant is not willing to consent for their child\'s participation.')
        if citizen == NO:
            self.error_message.append(
                'Participant is not a Botswana citizen.')
        self.is_eligible = False if self.error_message else True


class CaregiverChildConsentEligibility:

    def __init__(self, child_test=None, child_remain_in_study=None,
                 child_preg_test=None, child_knows_status=None):
        self.error_message = []
        self.child_test = child_test
        self.child_remain_in_study = child_remain_in_study
        self.child_preg_test = child_preg_test
        self.child_knows_status = child_knows_status
        if self.child_test == NO:
            self.error_message.append(
                'Participant is not willing to allow for HIV testing and '
                'counselling of child.')
        if self.child_remain_in_study == NO:
            self.error_message.append(
                'Child is not will to remain in the study area.')
        if self.child_preg_test == NO:
            self.error_message.append(
                'Participant will not allow the child to undergo pregnancy testing.')
        if self.child_knows_status == NO:
            self.error_message.append(
                'Child has not been told about the mother\'s HIV status.')
        self.is_eligible = False if self.error_message else True
