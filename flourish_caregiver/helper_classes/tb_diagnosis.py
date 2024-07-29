from edc_constants.constants import NEG, NO, POS, YES


class TBDiagnosis:
    EVALUATION_CONDITION = '>= 2 weeks'

    def __init__(self, child_age=None, hiv_status=None):
        self.child_age = child_age
        self.hiv_status = hiv_status

    def evaluate_screening_conditions(self, screening):
        return sum([
            screening.cough_duration == self.EVALUATION_CONDITION,
            screening.fever_duration == self.EVALUATION_CONDITION,
            screening.sweats_duration == self.EVALUATION_CONDITION,
            screening.weight_loss_duration == self.EVALUATION_CONDITION,
            (screening.evaluated_for_tb == NO and
             screening.household_diagnosed_with_tb == YES)
        ]) >= 1

    def evaluate_for_tb(self, screening):
        if self.child_age:
            if self.child_age <= 12:
                return ((screening.evaluated_for_tb == NO and
                         screening.household_diagnosed_with_tb == YES) or
                        screening.cough_duration == self.EVALUATION_CONDITION or
                        screening.fever_duration == self.EVALUATION_CONDITION or
                        screening.weight_loss_duration == self.EVALUATION_CONDITION or
                        screening.fatigue_or_reduced_playfulness == YES)
            elif self.child_age > 12:
                return self.evaluate_screening_conditions(screening)
        if self.hiv_status == NEG:
            return self.evaluate_screening_conditions(screening)
        elif self.hiv_status == POS:
            return (
                    screening.cough == YES or
                    screening.fever == YES or
                    screening.sweats == YES or
                    screening.weight_loss == YES or
                    (screening.evaluated_for_tb == NO and
                     screening.household_diagnosed_with_tb == YES)
            )
