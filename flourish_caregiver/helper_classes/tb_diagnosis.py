from edc_constants.constants import NO, POS, YES


class TBDiagnosis:
    def __init__(self, child_age=None, hiv_status=None):
        self.child_age = child_age
        self.hiv_status = hiv_status

    def evaluate_for_tb(self, screening):
        if self.child_age:
            if self.child_age <= 12:
                return (screening.evaluated_for_tb == NO or sum(
                    [screening.cough_duration == '>= 2 weeks',
                     screening.fever_duration == '>= 2 weeks',
                     screening.weight_loss_duration == '>= 2 weeks',
                     screening.fatigue_or_reduced_playfulness == YES]) >= 2)
            elif self.child_age > 12:
                return (sum([screening.cough_duration == '>= 2 weeks',
                             screening.fever_duration == '>= 2 weeks',
                             screening.sweats_duration == '>= 2 weeks',
                             screening.weight_loss_duration == '>= 2 weeks',
                             screening.evaluated_for_tb == NO]) >= 1)
        if self.hiv_status == POS:
            return (sum([screening.cough_duration == '>= 2 weeks',
                         screening.fever_duration == '>= 2 weeks',
                         screening.sweats_duration == '>= 2 weeks',
                         screening.weight_loss_duration == '>= 2 weeks',
                         screening.evaluated_for_tb == NO]) >= 1)
        else:
            return (sum([screening.cough == YES,
                         screening.fever == YES,
                         screening.sweats == YES,
                         screening.weight_loss == YES,
                         screening.evaluated_for_tb == NO]) >= 1)
