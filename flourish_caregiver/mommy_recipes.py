from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from edc_constants.constants import ALIVE, FEMALE, NEG, NO, NOT_APPLICABLE, ON_STUDY, \
    PARTICIPANT, POS, YES
from edc_visit_tracking.constants import SCHEDULED
from faker import Faker
from model_mommy.recipe import Recipe, seq

from flourish_caregiver.models.hiv_disclosure_status import HIVDisclosureStatusA
from flourish_caregiver.models.tb_engagement import TbEngagement
from .models import AntenatalEnrollment, MaternalDelivery, SubjectConsent, \
    TbInformedConsent, TbInterview, TbOffStudy, TbStudyEligibility, TbVisitScreeningWomen
from .models import CaregiverChildConsent, HIVRapidTestCounseling, LocatorLogEntry
from .models import CaregiverEdinburghDeprScreening, CaregiverGadAnxietyScreening, \
    CaregiverPhqDeprScreening, TbRoutineHealthScreenV2
from .models import CaregiverLocator, MaternalDataset, MaternalVisit, \
    RelationshipFatherInvolvement
from .models import CaregiverPhqReferral, FlourishConsentVersion
from .models import CaregiverPreviouslyEnrolled
from .models import ScreeningPregWomen, ScreeningPriorBhpParticipants, UltraSound
from .models import MaternalInterimIdccVersion2
from .models import InterviewFocusGroupInterestV2

fake = Faker()

# father involement

relationshipfatherinvolvement = Recipe(
    RelationshipFatherInvolvement,
)

maternaldataset = Recipe(
    MaternalDataset,
)

caregiverlocator = Recipe(
    CaregiverLocator,
    first_name=fake.first_name,
    last_name=fake.last_name,
    user_created='flourish')

locatorlogentry = Recipe(
    LocatorLogEntry,
    report_datetime=get_utcnow(),
    log_status='exist',
    user_created='flourish')

screeningpriorbhpparticipants = Recipe(
    ScreeningPriorBhpParticipants,
    child_alive=YES,
    flourish_participation='interested')

screeningpregwomen = Recipe(
    ScreeningPregWomen,
    hiv_testing=YES,
    breastfeed_intent=YES)

flourishconsentversion = Recipe(
    FlourishConsentVersion,
)

subjectconsent = Recipe(
    SubjectConsent,
    subject_identifier=None,
    consent_datetime=get_utcnow(),
    dob=get_utcnow() - relativedelta(years=27),
    first_name=fake.first_name,
    last_name=fake.last_name,
    initials='XX',
    gender='F',
    identity=seq('123427675'),
    confirm_identity=seq('123427675'),
    identity_type='country_id',
    is_dob_estimated='-',
    hiv_testing=YES,
    remain_in_study=YES,
    consent_reviewed=YES,
    study_questions=YES,
    consent_signature=YES,
    consent_copy=YES,
    future_contact=YES,
    child_consent=YES,
    citizen=YES,
    version='1'
)

tbinformedconsent = Recipe(
    TbInformedConsent,
    first_name=fake.first_name,
    last_name=fake.last_name,
    identity=seq('123427675'),
    confirm_identity=seq('123427675'),
    is_literate=YES,
    consent_to_participate=YES,
)

caregiverpreviouslyenrolled = Recipe(
    CaregiverPreviouslyEnrolled,
    maternal_prev_enroll=YES,
    sex=FEMALE,
    current_hiv_status=NEG)

caregiverchildconsent = Recipe(
    CaregiverChildConsent,
    first_name=fake.first_name,
    last_name=fake.last_name,
    subject_identifier=None,
    gender='M',
    child_test=YES,
    child_dob=(get_utcnow() - relativedelta(years=3)).date(),
    child_remain_in_study=YES,
    child_preg_test=NOT_APPLICABLE,
    child_knows_status=YES,
    identity=seq('234513187'),
    identity_type='birth_cert',
    confirm_identity=seq('234513187')
)

antenatalenrollment = Recipe(
    AntenatalEnrollment,
    report_datetime=get_utcnow(),
    current_hiv_status=POS,
    date_at_32wks=(get_utcnow() - relativedelta(months=3)).date(),
    edd_by_lmp=(get_utcnow() + relativedelta(months=4)).date(),
    enrollment_hiv_status=POS,
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
    HIVRapidTestCounseling, )

gadanxietyscreening = Recipe(
    CaregiverGadAnxietyScreening,
    feeling_anxious='1',
    control_worrying='3',
    worrying='1',
    trouble_relaxing='0',
    restlessness='1',
    easily_annoyed='2',
    fearful='3', )

caregiverphqdeprscreening = Recipe(
    CaregiverPhqDeprScreening,
    activity_interest='1',
    depressed='2',
    sleep_disorders='1',
    fatigued='0',
    eating_disorders='0',
    self_doubt='0',
    easily_distracted='1',
    restlessness='1',
    self_harm='0', )

caregiverphqreferral = Recipe(
    CaregiverPhqReferral)

caregiveredinburghdeprscreening = Recipe(
    CaregiverEdinburghDeprScreening,
    able_to_laugh='0',
    enjoyment_to_things='0',
    self_blame='2',
    anxious='3',
    panicky='1',
    coping='1',
    sleeping_difficulty='2',
    miserable_feeling='1',
    unhappy='1',
    self_harm='1', )

hivrapidtest = Recipe(
    HIVRapidTestCounseling, )

hivdisclosurestatusa = Recipe(
    HIVDisclosureStatusA, )

tbstudyeligibility = Recipe(
    TbStudyEligibility, )

tboffstudy = Recipe(
    TbOffStudy,
)

tbvisitscreeningwomen = Recipe(
    TbVisitScreeningWomen,
)

tbengagement = Recipe(
    TbEngagement,
)

ultrasound = Recipe(
    UltraSound
)

tbinterview = Recipe(
    TbInterview,
)

maternalinterimidccversion2 = Recipe(
    MaternalInterimIdccVersion2, )

tbroutinehealthscreenv2 = Recipe(
    TbRoutineHealthScreenV2, )


interviewfocusgroupinterestv2 = Recipe(
    InterviewFocusGroupInterestV2, )
