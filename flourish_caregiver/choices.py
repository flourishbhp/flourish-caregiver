from edc_constants.constants import (
    OFF_STUDY, ON_STUDY, FAILED_ELIGIBILITY, PARTICIPANT)
from edc_constants.constants import ALIVE, DEAD, NOT_APPLICABLE, OTHER, UNKNOWN
from edc_constants.constants import YES, NO, POS, NEG
from edc_visit_tracking.constants import MISSED_VISIT, COMPLETED_PROTOCOL_VISIT
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT

from .constants import BREASTFEED_ONLY, NEVER_STARTED, MODIFIED, TUBERCULOSIS
from .constants import NO_MODIFICATIONS, START

ABLE_TO_LAUGH = (
    ('0', 'As much as I always could'),
    ('1', 'Not quite so much now'),
    ('2', 'Definitely not so much now'),
    ('3', 'Not at all'),
)

AGITATION = (
    ('0', 'None'),
    ('1', 'Fidgetiness'),
    ('2', 'Playing with hands, hair, etc.'),
    ('3', 'Moving about, can’t sit still.'),
    ('4', 'Hand wringing, nail biting, hair-pulling, biting of lips.')
)

ALIVE_DEAD_UNKNOWN = (
    (ALIVE, 'Alive'),
    (DEAD, 'Dead'),
    (UNKNOWN, 'Unknown'),
)

AMNIOTIC_FLUID = (
    ('0', 'Normal'),
    ('1', 'Abnormal')
)

ANXIETY_PYSCHIC = (
    ('0', 'No difficulty'),
    ('1', 'Subjective tension and irritability'),
    ('2', 'Worrying about minor matters'),
    ('3', 'Apprehensive attitude apparent in face or speech'),
    ('4', 'Fears expressed without questioning')
)

ANXIETY = (
    ('0', 'Absent'),
    ('1', 'Mild'),
    ('2', 'Moderate'),
    ('3', 'Severe'),
    ('4', 'Incapacitating')
)

ANXIOUS = (
    ('0', 'No, not at all'),
    ('1', 'Hardly ever'),
    ('2', 'Yes, sometimes'),
    ('3', 'Yes, very often')
)

ARV_DRUG_LIST = (
    ('Abacavir', 'ABC'),
    ('Zidovudine', 'AZT'),
    ('Tenoforvir', 'TDF'),
    ('Lamivudine', '3TC'),
    ('Emtricitabine', 'FTC'),
    #     ('Didanosine', 'DDI'),
    #     ('Stavudine', 'D4T'),
    ('Nevirapine', 'NVP'),
    ('Efavirenz', 'EFV'),
    #     ('Lopinavir', 'LPV'),
    ('Aluvia', 'ALU'),
    #     ('Atazanavir', 'ATV'),
    #     ('Ritonavir', 'RTV'),
    #     ('Raltegravir', 'RAL'),
    ('Dolutegravir', 'DTG'),
    #     ('Nelfinavir', 'NFV'),
    ('HAART,unknown', 'HAART,unknown'),
)

ARV_INTERRUPTION_REASON = (
    ('TOXICITY', 'Toxicity'),
    ('NO_DRUGS', 'No drugs available'),
    ('NO_REFILL', 'Didn\'t get to clinic for refill'),
    ('FORGOT', 'Mother forgot to take the ARVs'),
    (OTHER, 'Other'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

CONSENT_VERSION = (
    ('1', 'Consent version 1'),
    ('3', 'Consent version 3')
)

CONTACT_FAIL_REASON = (
    ('no_response', 'Phone rang, no response but voicemail left'),
    ('no_response_vm_not_left', 'Phone rang no response and no option to leave voicemail'),
    ('disconnected', 'Phone did not ring/number disconnected'),
    ('number_changed', 'No longer the phone number of BHP participant'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

CONTACT_MODE = (
    ('phone_call', 'Phone Call'),
    ('house_visit', 'Visit to household'),
    (OTHER, 'Other'),
)

COWS_MILK = (
    ('boiled', '1. Boiled from cow'),
    ('unboiled', '2. Unboiled from cow'),
    ('store', '3. From store'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

CRYING = (
    ('3', 'Yes, most of the time'),
    ('2, quite often', 'Yes, quite often'),
    ('1', 'Only occasionally'),
    ('0', 'No, never')
)

DEPRESSION_SCALE = (
    ('0', 'Not at all'),
    ('1', 'Several days'),
    ('2', 'More than half the days'),
    ('3', 'Nearly every day'),
)

DEPRESSION_MOOD = (
    ('0', 'Absent'),
    ('1', 'These feeling states indicated only on questioning'),
    ('2', 'These feeling states spontaneously reported verbally'),
    ('3', ('Communicates feeling states non-verbally, i.e. through facial '
           'expression, posture, voice and tendency to weep')),
    ('4', ('Patient reports virtually only these feeling states in his/her '
           'spontaneous verbal and non-verbal communication.'))
)

ENJOYMENT_TO_THINGS = (
    ('0', 'As much as I ever did'),
    ('1', 'Rather less than I used to'),
    ('2', 'Definitely less than I used to'),
    ('3', 'Hardly at all'),
)

FEEDING_CHOICES = (
    (BREASTFEED_ONLY, 'Breastfeed only'),
    ('Formula feeding only', 'Formula feeding only'),
    ('Both breastfeeding and formula feeding',
     'Both breastfeeding and formula feeding'),
    ('Medical complications: Infant did not feed',
     'Medical complications: Infant did not feed'),
)

FOOD_FREQUENCY = (
    ('0', 'Often True'),
    ('1', 'Sometimes True'),
    ('2', 'Never True'),
    ("3", "I don’t know or Refused to answer"),
)

GENERAL_SOMATIC = (
    ('0', 'None'),
    ('1', ('Heaviness in limbs, back or head. Backaches, headaches, '
           'muscle aches. Loss of energy and fatigability.')),
    ('2', ('Any clear-cut symptom rates 2.')),
)

GENITAL_SYMPTOMS = (
    ('0', 'Absent'),
    ('1', 'Mild'),
    ('2', 'Severe')
)

GESTATIONS_NUMBER = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3')
)

GUILT_FEELINGS = (
    ('0', 'Absent'),
    ('1', 'Self-reproach, feels he/she has let people down'),
    ('2', 'Ideas of guilt or rumination over past errors or sinful deeds.'),
    ('3', 'Present illness is a punishment; delusions of guilt'),
    ('4', 'Hears accusatory or denunciatory voices and/or experiences threatening visual hallucinations.')
)

HARM = (
    ('3', 'Yes, quite often'),
    ('2', 'Sometimes'),
    ('1', 'Hardly ever'),
    ('0', 'Never')
)

HOME_VISIT_FAIL = (
    ('no_one_home', 'No one was home'),
    ('relocated', 'Previous BHP participant no longer lives at household'),
    (OTHER, 'Other')
)

HOW_OFTEN = (
    ('0', 'Acknowledges being depressed and ill'),
    ('1', 'Acknowledges illness but attributes cause to bad food, climate, '
          'overwork, virus, need for rest, etc'),
    ('2', 'Denies being ill at all'),
)

HYPOCHONDRIASIS = (
    ('0', 'Not present'),
    ('1', 'Self-absorption (bodily)'),
    ('2', 'Preoccupation with health'),
    ('3', 'Frequent complaints, requests for help, etc.'),
    ('4', 'Hypochondriacal delusions')
)

IDENTITY_TYPE = (
    ('country_id', 'Country ID number'),
    ('country_id_rcpt', 'Country ID receipt'),
    ('passport', 'Passport'),
    (OTHER, 'Other'),
)

INFO_PROVIDER = (
    ('MOTHER', 'Mother'),
    ('GRANDMOTHER', 'Grandmother'),
    ('FATHER', 'Father'),
    ('GRANDFATHER', 'Grandfather'),
    ('SIBLING', 'Sibling'),
    (OTHER, 'Other'),
)

INSIGHT = (
    ('0', 'Acknowledges being depressed and ill'),
    ('1', ('Acknowledges illness but attributes cause to bad food, climate, '
           'overwork, virus, need for rest, etc')),
    ('2', 'Denies being ill at all')
)

INSOMNIA_INITIAL = (
    ('0', 'No difficulty falling asleep.'),
    ('1', 'Complains of occasional difficulty falling asleep, i.e. more than 1⁄2 hour.'),
    ('2', 'Complains of nightly difficulty falling asleep')
)

INSOMIA_MIDNIGHT = (
    ('0', 'No difficulty.'),
    ('1', 'Patient complains of being restless and disturbed during the night.'),
    ('2', 'Waking during the night – any getting out of bed rates 2 (except for purposes of voiding).')
)

INSOMNIA_EARLY = (
    ('0', 'No difficulty.'),
    ('1', 'Waking in early hours of the morning but goes back to sleep.'),
    ('2', 'Unable to fall asleep again if he/she gets out of bed.'),
)

LOCATOR_LOG_STATUS = (
    ('exist', 'Exists'),
    ('not_found', 'Not found')
    )

MATERNAL_VISIT_STUDY_STATUS = (
    (ON_STUDY, 'On study'),
    (OFF_STUDY,
     'Off study-no further follow-up (including death); use only '
     'for last study contact'),
)

MEALS = (
    ('0', 'Yes'),
    ('1', 'No'),
    ("2", "I don’t know"),
)

MISERABLE_FEELING = (
    ('0', 'No, not at all'),
    ('1', 'Not very often'),
    ('2', 'Yes, quite often'),
    ('3', 'Yes, most of the time'),
)

PANICK = (
    ('3', 'Yes, quite a lot'),
    ('2, sometimes', 'Yes, sometimes'),
    ('1', 'No, not much'),
    ('0', 'No, not at all')
)

REASON_ARV_STOP = (
    ('switch for tolerability', 'Switch for tolerability'),
    ('switch for drug outage', 'Switch for drug outage'),
    ('Treatment failure', 'Treatment failure'),
    (OTHER, 'Other, specify:')
)

REASONS_VACCINES_MISSED = (
    ('missed scheduled vaccination', 'Mother or Caregiver has not '
     'yet taken infant '
        'to clinic for this scheduled vaccination'),
    ('caregiver declines vaccination',
     'Mother or Caregiver declines this vaccicnation'),
    ('no stock', 'Stock out at clinic'),
    (OTHER, 'Other, specify'),
)

REFERRED_TO = (
    ('community_social_worker', 'Community Social Worker'),
    ('hospital_based_social_worker', 'Hospital-based Social Worker'),
    ('a&e', 'A&E'),
    ('psychologist', 'Psychologist'),
    ('psychiatrist', 'Psychiatrist'),
    (OTHER, 'Other'),
)

RELATION_TO_CHILD = (
    ('father', 'Father'),
    ('grandmother', 'Grandmother'),
    ('grandfather', 'Grandfather'),
    ('aunt', 'Aunt'),
    ('uncle', 'Uncle'),
    ('sister', 'Sister'),
    ('brother', 'Brother'),
    ('guardian', 'Guardian'),
    (OTHER, 'Other'),
)

RETARDATION = (
    ('0', 'Normal speech and thought.'),
    ('1', 'Slight retardation during the interview.'),
    ('2', 'Obvious retardation during the interview.'),
    ('3', 'Interview difficult'),
    ('4', 'Complete stupor')
)

SLEEPING_DIFFICULTY = (
    ('0', 'No, not at all'),
    ('1', 'Not very often'),
    ('2', 'Yes, sometimes'),
    ('3', 'Yes, most of the time'),
)

SELF_BLAME = (
    ('0', 'No, never'),
    ('1', 'Not very often'),
    ('2', 'Yes, some of the time'),
    ('3', 'Yes, most of the time'),
)

SOMATIC_SYMPTOMS = (
    ('0', 'None'),
    ('1', 'Loss of appetite but eating without staff encouragement. Heavy feelings in abdomen.'),
    ('2', ('Difficulty eating without staff urging. Requests or requires '
           'laxatives or medication for bowels or medication for gastro-intestinal symptoms.')),
)

SUICIDAL = (
    ('0', 'Absent'),
    ('1', 'Feels life is not worth living'),
    ('2', 'Wishes he/she were dead or any thoughts of possible death to self.'),
    ('3', 'Suicidal ideas or gestures'),
    ('4', 'Attempts at suicide')
)

TIMES_BREASTFED = (
    ('<1 per week', '1. Less than once per week'),
    ('<1 per day, but at least once per week',
     '2. Less than once per day, but at least once per week'),
    ('about 1 per day on most days', '3. About once per day on most days'),
    ('>1 per day, but not for all feedings',
     '4. More than once per day, but not for all feedings'),
    ('For all feedings',
     '5. For all feedings (i.e no formula or other foods or liquids)'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

TOP = (
    ('3', 'Yes, most of the time I haven\'t been able to cope at all'),
    ('2', 'Yes, sometimes I haven\'t been coping as well as usual'),
    ('1', 'No, most of the time I have coped quite well'),
    ('0', 'No, I have been coping as well as ever')
)

TRISOME_CHROSOMESOME_ABNORMALITY = (
    ('None', 'None'),
    ('Trisomy 21', 'Trisomy 21'),
    ('Trisomy 13', 'Trisomy 13'),
    ('Trisomy 18', 'Trisomy 18'),
    ('OTHER trisomy, specify', 'Other trisomy, specify'),
    ('OTHER non-trisomic chromosome',
     'Other non-trisomic chromosome abnormality, specify'),
)

WATER_USED = (
    ('Water direct from source', 'Water direct from source'),
    ('Water boiled immediately before use',
     'Water boiled immediately before use'),
    ('Water boiled earlier and then stored',
     'Water boiled earlier and then stored'),
    ('Specifically treated water', 'Specifically treated water'),
    (OTHER, 'Other (specify)'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

WORK_INTERESTS = (
    ('0', 'No difficulty'),
    ('1', ('Thoughts and feelings of incapacity, fatigue or weakness related to'
           ' activities, work or hobbies.')),
    ('2', ('Loss of interest in activity, hobbies or work – either directly '
           'reported by the patient or indirect in listlessness, indecision and vacillations')),
    ('3', 'Decrease in actual time spent in activities or decrease in productivity'),
    ('4', ('Stopped working because of present illness.'))
)

WEIGHT_LOSS = (
    ('0', 'No weight loss'),
    ('1', 'Probable weight loss associated with present illness.'),
    ('2', 'Definite (according to patient) weight loss.'),
    ('3', 'Not assessed.')
)

VISIT_INFO_SOURCE = [
    (PARTICIPANT, 'Clinic visit with participant'),
    ('other_contact',
     'Other contact with participant (for example telephone call)'),
    ('other_doctor',
     'Contact with external health care provider/medical doctor'),
    ('family',
     'Contact with family or designated person who can provide information'),
    ('chart', 'Hospital chart or other medical record'),
    (OTHER, 'Other')]

VISIT_REASON = [
    (SCHEDULED, 'Scheduled visit/contact'),
    (MISSED_VISIT, 'Missed Scheduled visit'),
    (UNSCHEDULED,
     'Unscheduled visit at which lab samples or data are being submitted'),
    (LOST_VISIT, 'Lost to follow-up (use only when taking subject off study)'),
    (FAILED_ELIGIBILITY, 'Subject failed enrollment eligibility'),
    (COMPLETED_PROTOCOL_VISIT, 'Subject has completed the study')]


ZERO_ONE = (
    ('0', '0'),
    ('1', '1')
)
