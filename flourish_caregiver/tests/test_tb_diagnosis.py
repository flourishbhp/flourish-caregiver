from django.test import TestCase, tag
from edc_constants.constants import NEG, NO, POS, YES

from flourish_caregiver.helper_classes.tb_diagnosis import TBDiagnosis


@tag('tbdia')
class TestTBDiagnosis(TestCase):
    def setUp(self):
        self.child_age = None
        self.hiv_status = None
        self.tb_diagnosis = TBDiagnosis(self.child_age, self.hiv_status)

    def test_evaluate_for_tb_child_age_under_12(self):
        self.tb_diagnosis.child_age = 10
        screening = lambda: None
        screening.evaluated_for_tb = NO
        screening.cough_duration = '>= 2 weeks'
        screening.fever_duration = '< 2 weeks'
        screening.weight_loss_duration = '< 2 weeks'
        screening.fatigue_or_reduced_playfulness = NO
        self.assertEqual(self.tb_diagnosis.evaluate_for_tb(screening), True)

    def test_evaluate_for_tb_child_age_over_12(self):
        self.tb_diagnosis.child_age = 13
        screening = lambda: None
        screening.cough_duration = '< 2 weeks'
        screening.fever_duration = '< 2 weeks'
        screening.weight_loss_duration = '< 2 weeks'
        screening.sweats_duration = '< 2 weeks'
        screening.evaluated_for_tb = YES
        self.assertEqual(self.tb_diagnosis.evaluate_for_tb(screening), False)

    def test_evaluate_for_tb_hiv_POS_caregiver(self):
        self.tb_diagnosis.hiv_status = POS
        screening = lambda: None
        screening.cough_duration = '>= 2 weeks'
        screening.fever_duration = '>= 2 weeks'
        screening.weight_loss_duration = '>= 2 weeks'
        screening.sweats_duration = '>= 2 weeks'
        screening.evaluated_for_tb = YES
        self.assertEqual(self.tb_diagnosis.evaluate_for_tb(screening), True)

    def test_evaluate_for_tb_hiv_NEG_caregiver(self):
        self.tb_diagnosis.hiv_status = NEG
        screening = lambda: None
        screening.cough = YES
        screening.fever = NO
        screening.sweats = YES
        screening.weight_loss = YES
        screening.evaluated_for_tb = YES
        self.assertEqual(self.tb_diagnosis.evaluate_for_tb(screening), True)
