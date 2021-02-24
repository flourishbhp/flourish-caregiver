from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, NO, POS
from edc_visit_tracking.constants import SCHEDULED
from edc_constants.constants import ALIVE, YES, NO, ON_STUDY, PARTICIPANT
from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import AntenatalEnrollment, SubjectConsent, MaternalVisit
from .models import MaternalDelivery, HIVRapidTestCounseling, MaternalDataset
from .models import CaregiverChildConsent


fake = Faker()

maternaldataset = Recipe(
    MaternalDataset)

subjectconsent = Recipe(
    SubjectConsent,
    subject_identifier=None,
    consent_datetime=get_utcnow(),
    dob=get_utcnow() - relativedelta(years=25),
    first_name=fake.first_name,
    last_name=fake.last_name,
    initials='XX',
    gender='F',
    identity=seq('123425678'),
    confirm_identity=seq('123425678'),
    identity_type='OMANG',
    is_dob_estimated='-',
    version='1'
)

caregiverchildconsent = Recipe(
    CaregiverChildConsent,
    identity=seq('123425678'),
    confirm_identity=seq('123425678'),
    version='1')

antenatalenrollment = Recipe(
    AntenatalEnrollment,
    report_datetime=get_utcnow(),
    current_hiv_status=POS,
    date_at_32wks=(get_utcnow() - relativedelta(months=3)).date(),
    edd_by_lmp=(get_utcnow() + relativedelta(months=4)).date(),
    enrollment_hiv_status=POS,
    evidence_32wk_hiv_status=YES,
    evidence_hiv_status=YES,
    ga_lmp_anc_wks=26,
    ga_lmp_enrollment_wks=24,
    is_diabetic=NO,
    is_eligible=True,
    knows_lmp=YES,
    last_period_date=(get_utcnow() - relativedelta(months=6)).date(),
    pending_ultrasound=False,
    rapid_test_date=None,
    rapid_test_done='N/A',
    rapid_test_result=None,
    week32_result=None,
    week32_test=YES,
    week32_test_date=(get_utcnow() - relativedelta(months=2)).date(),
    will_breastfeed=YES,
    will_get_arvs=YES)

maternalvisit = Recipe(
    MaternalVisit,
    report_datetime=get_utcnow(),
    reason=SCHEDULED,
    study_status=ON_STUDY,
    survival_status=ALIVE,
    info_source=PARTICIPANT)

maternaldelivery = Recipe(
    MaternalDelivery,
    subject_identifier=None,)

hivrapidtestcounseling = Recipe(
    HIVRapidTestCounseling,)
