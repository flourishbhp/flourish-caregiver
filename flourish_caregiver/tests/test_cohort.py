from dateutil.relativedelta import relativedelta
from datetime import date

from django.test.testcases import TestCase
from  django.utils import timezone


class TestCohort(TestCase):

    def setUp(self):
        self.data = {
            'enrollment_date': timezone.now().date(),
            'child_dob': date.today() - relativedelta(years=2),
            'infant_hiv_exposed': 'Exposed',
            'mum_hivstatus': None,
            'protocol': 'Tshilo Dikotla'
        }

    def test_calculate_age(self):
        """Test if """
