from django.test.testcases import TestCase
from datetime import datetime

from ..models import MaternalDataset, LocatorLog


class TestLocatorLogs(TestCase):

    def setUp(self):
        self.options = {
            'cooking_method': '',
            'delivdt': datetime(2015, 3, 31).date(),
            'delivery_location': 'Molepolole',
            'delivmeth': '',
            'house_type': 'Formal: tin-roofed & concrete walls',
            'live_inhouse_number': 5,
            'mom_age_enrollment': '18-24 years',
            'mom_arvstart_date': datetime(2014, 6, 17).date(),
            'mom_baseline_cd4': 516,
            'mom_education': 'Secondary',
            'mom_enrolldate': datetime(2015, 4, 1).date(),
            'mom_hivstatus': 'HIV-infected',
            'mom_maritalstatus': 'Single',
            'mom_moneysource': 'Relative',
            'mom_occupation': 'Housewife or unemployed',
            'mom_personal_earnings': 'None',
            'mom_pregarv_strat': '3-drug ART',
            'parity': 1,
            'piped_water': 'Other water source',
            'protocol': '4',
            'site_name': 'Gaborone',
            'study_maternal_identifier': '056-49956',
            'toilet': 2,
            'toilet_indoors': 'Latrine or none',
            'toilet_private': 'Indoor toilet or private latrine'}

    def test_create_locator_log(self):
        """Test if a maternal dataset creates a locator log instance.
        """
        maternal_dataset = MaternalDataset.objects.create(**self.options)
        self.assertEqual(LocatorLog.objects.filter(
            maternal_dataset=maternal_dataset).count(), 1)
