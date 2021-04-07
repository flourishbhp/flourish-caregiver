from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import ALIVE, YES, NO, POS, ON_STUDY, PARTICIPANT, NOT_APPLICABLE
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import AntenatalEnrollment, SubjectConsent, MaternalDelivery
from .models import MaternalDataset, CaregiverLocator, MaternalVisit
from .models import ScreeningPregWomen, ScreeningPriorBhpParticipants
from .models import HIVRapidTestCounseling, LocatorLogEntry, CaregiverChildConsent
from .models import CaregiverGadAnxietyScreening


fake = Faker()

maternaldataset = Recipe(
    MaternalDataset,
    )

caregiverlocator = Recipe(
    CaregiverLocator)

locatorlogentry = Recipe(
    LocatorLogEntry,
    report_datetime=get_utcnow(),
    log_status='exist')

screeningpriorbhpparticipants = Recipe(
    ScreeningPriorBhpParticipants,
    child_alive=YES,
    flourish_interest=YES,
    flourish_participation='interested')

screeningpregwomen = Recipe(
    ScreeningPregWomen,
    hiv_testing=YES,
    breastfeed_intent=YES)

subjectconsent = Recipe(
    SubjectConsent,
    subject_identifier=None,
    consent_datetime=get_utcnow(),
    dob=get_utcnow() - relativedelta(years=27),
    first_name=fake.first_name,
    last_name=fake.last_name,
    initials='XX',
    gender='F',
    identity=seq('123427681'),
    confirm_identity=seq('123427681'),
    identity_type='country_id',
    is_dob_estimated='-',
    hiv_testing=YES,
    remain_in_study=YES,
    consent_reviewed=YES,
    study_questions=YES,
    assessment_score=YES,
    consent_signature=YES,
    consent_copy=YES,
    future_contact=YES,
    child_consent=YES,
    citizen=YES,
    version='1'
)

caregiverchildconsent = Recipe(
    CaregiverChildConsent,
    first_name=fake.first_name,
    last_name=fake.last_name,
    subject_identifier=None,
    gender='M',
    child_test=YES,
    child_dob=get_utcnow() - relativedelta(years=5),
    child_remain_in_study=YES,
    child_preg_test=NOT_APPLICABLE,
    child_knows_status=YES,
    identity=seq('123417681'),
    identity_type='birth_cert',
    confirm_identity=seq('123417681')
    )

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
    last_period_date=(get_utcnow() - relativedelta(months=5, weeks=3)).date(),
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
    subject_identifier=None,
    report_datetime=get_utcnow(),
    delivery_datetime=get_utcnow(),
    delivery_time_estimated=NO,
    labour_hrs='3',
    delivery_hospital='Lesirane',
    mode_delivery='spontaneous vaginal',
    csection_reason=NOT_APPLICABLE,
    live_infants_to_register=1,
    valid_regiment_duration=YES)

hivrapidtestcounseling = Recipe(
    HIVRapidTestCounseling,)

gadanxietyscreening = Recipe(
    CaregiverGadAnxietyScreening,
    feeling_anxious='1',
    control_worrying='3',
    worrying='1',
    trouble_relaxing='0',
    restlessness='1',
    easily_annoyed='2',
    fearful='3',)
