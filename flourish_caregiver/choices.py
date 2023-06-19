from django.utils.translation import ugettext_lazy as _
from edc_constants.constants import ALIVE, DEAD, NOT_APPLICABLE, OTHER, UNKNOWN, \
    FAILED_ELIGIBILITY, PARTICIPANT, DWTA, POS, NEG, ON_STUDY, OFF_STUDY, MALE, FEMALE, \
    NEVER, DONT_KNOW, PENDING, IND
from edc_constants.constants import YES, NO
from edc_visit_tracking.constants import MISSED_VISIT, COMPLETED_PROTOCOL_VISIT
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT

from flourish_caregiver.constants import NONE, PNTA, BREASTFEED_ONLY


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

STUDY_SITES = (
    ('40', 'Gaborone'),
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
    ('Nevirapine', 'NVP'),
    ('Efavirenz', 'EFV'),
    ('Aluvia', 'ALU'),
    ('Dolutegravir', 'DTG'),
    ('HAART,unknown', 'HAART,unknown'),
)

ARV_INTERRUPTION_REASON = (
    ('TOXICITY', 'Toxicity'),
    ('NO_DRUGS', 'No drugs available'),
    ('NO_REFILL', 'Didn\'t get to clinic for refill'),
    ('FORGOT', 'Mother forgot to take the ARVs'),
    ('DEFAULT', 'Defaulted ARV treatment (7 days or more)'),
    ('TOLERABILITY', 'Switch for tolerability'),
    ('FAILURE', 'Treatment failure'),
    (OTHER, 'Other'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

ARV_INTERRUPTION_REASON_POST_ADHERENCE = (
    ('TOXICITY_SELF', 'Toxicity, discontinued by self'),
    ('TOXICITY_HEALTHCARE_PROVIDER', 'Toxicity, discontinued by healthcare provider'),
    ('NO_DRUGS', 'No drugs available'),
    ('NO_REFILL', 'Didn\'t get to clinic for refill'),
    ('FORGOT', 'Participant forgot to take the ARVs'),
    ('TRAVELING', 'Participant was traveling'),
    ('DEFAULT', 'Defaulted ARV treatment (7 days or more)'),
    (OTHER, 'Other'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

CHILD_IDENTITY_TYPE = (
    ('country_id', 'Country ID number'),
    ('birth_cert', 'Birth Certificate number'),
    ('country_id_rcpt', 'Country ID receipt'),
    ('passport', 'Passport'),
    (OTHER, 'Other'),
)

COHORTS = (
    ('cohort_a', 'Cohort A'),
    ('cohort_b', 'Cohort B'),
    ('cohort_c', 'Cohort C'),
    ('cohort_a_sec', 'Cohort A Secondary Aims'),
    ('cohort_b_sec', 'Cohort B Secondary Aims'),
    ('cohort_c_sec', 'Cohort C Secondary Aims'),
    ('cohort_pool', 'Cohort Pool'),)

CONSENT_VERSION = (
    ('1', 'Consent version 1'),
    ('2', 'Consent version 2'),
    ('3', 'Consent version 3')
)

CHILD_CONSENT_VERSION = (
    ('1', 'Consent version 1'),
    ('2', 'Consent version 2'),
    ('2.1', 'Consent version 2.1'),
    ('3', 'Consent version 3')
)

CONTACT_FAIL_REASON = (
    ('no_response', 'Phone rang, no response but voicemail left'),
    (
        'no_response_vm_not_left',
        'Phone rang no response and no option to leave voicemail'),
    ('disconnected', 'Phone did not ring/number disconnected'),
    ('number_changed', 'No longer the phone number of BHP participant'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

CONTACT_LOCATION = (
    ('phy_addr_unsuc', 'physical_address'),
    ('workplace_unsuc', 'subject_work_place'),
    ('contact_person_unsuc', 'indirect_contact_physical_address'),
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
    ('2', 'Yes, quite often'),
    ('1', 'Only occasionally'),
    ('0', 'No, never')
)

DECLINE_REASON = (
    ('cant_physically_attend', 'Not able to physically come to clinic'),
    ('not_interested', 'Not interested in participating'),
    (OTHER, 'Other (Specify)'),)

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

EMO_SUPPORT_PROVIDER = (
    ('psychologist', 'Psychologist'),
    ('hosp_social_worker', 'Hospital-based social worker'),
    ('comm_social_worker', 'Community Social worker'),
    ('psychiatrist', 'Psychiatrist'),
    (PNTA, _('Prefer not to answer')),)

ENJOYMENT_TO_THINGS = (
    ('0', 'As much as I ever did'),
    ('1', 'Rather less than I used to'),
    ('2', 'Definitely less than I used to'),
    ('3', 'Hardly at all'),
)

EXTRA_PULMONARY_LOC = (
    ('lymph_nodes', 'Lymph nodes'),
    ('abdomen', 'Abdomen '),
    ('bones', 'Bones '),
    ('brain', 'Brain'),
    (UNKNOWN, 'Unknown'),
)

FEEDING_CHOICES = (
    (BREASTFEED_ONLY, 'Breastfeed only'),
    ('Formula feeding only', 'Formula feeding only'),
    ('Both breastfeeding and formula feeding',
     'Both breastfeeding and formula feeding'),
    ('Medical complications: Infant did not feed',
     'Medical complications: Infant did not feed'),
)

FLOURISH_PARTICIPATION = (
    ('interested', 'Yes I am interested'),
    ('another_caregiver_interested', 'Yes another caregiver is interested'),
    (NO, 'No'),
    ('undecided', 'Undecided'),
    (NOT_APPLICABLE, 'Not applicable'),
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
    ('4', 'Hears accusatory or denunciatory voices and/or experiences threatening'
          ' visual hallucinations.')
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
    ('2',
     'Waking during the night – any getting out of bed rates 2 (except for purposes of voiding).')
)

INSOMNIA_EARLY = (
    ('0', 'No difficulty.'),
    ('1', 'Waking in early hours of the morning but goes back to sleep.'),
    ('2', 'Unable to fall asleep again if he/she gets out of bed.'),
)

LOCATION_FOR_CONTACT = (
    ('physical_address', 'Physical Address with detailed description'),
    ('workplace_location', 'Name and location of workplace'),
    ('contact_person', 'Full physical address '),
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
    ('2', "I don’t know"),
)

MISERABLE_FEELING = (
    ('0', 'No, not at all'),
    ('1', 'Not very often'),
    ('2', 'Yes, quite often'),
    ('3', 'Yes, most of the time'),
)

PANICK = (
    ('3', 'Yes, quite a lot'),
    ('2', 'Yes, sometimes'),
    ('1', 'No, not much'),
    ('0', 'No, not at all')
)

PHONE_NUM_TYPE = (
    ('cell_contact', 'Cell Phone'),
    ('alt_cell_contact', 'Cell Phone (alternative)'),
    ('tel_contact', 'Telephone'),
    ('alt_tel_contact', 'Telephone (alternative)'),
    ('work_contact', 'Work contact number'),
    ('cell_alt_contact', 'Alternative contact person cell phone'),
    ('tel_alt_contact', 'Alternative contact person telephone'),
    ('cell_resp_person', 'Responsible person cell phone'),
    ('tel_resp_person', 'Responsible person telephone'),
    (NONE, 'None')
)

REASON_ARV_STOP = (
    ('switch for tolerability', 'Switch for tolerability'),
    ('switch for drug outage', 'Switch for drug outage'),
    ('Treatment failure', 'Treatment failure'),
    (OTHER, 'Other, specify:')
)

REASONS_NOT_DISCLOSED = (
    ('fear_of_burdening_the_child', 'Fear of burdening the child'),
    ('stigma', 'Stigma'),
    ('fear_of_rejection', 'Fear of rejection'),
    ('feeling_child_is_immature', 'Feeling child is immature'),
    ('worry_about_her_mother', 'Does not want the child to worry about her mother'),
    ('scare_the_child', 'Does not want to scare the child'),
    ('hurt_by_reactions_of_others',
     'Does not want the child to be hurt by reactions of others'),
    ('feel_the_child_needs_to_know', 'Does not feel the child needs to know'),
    ('does_not_know_how_to_explain',
     'Does not know how to explain this to their child'),
    (OTHER, 'Other')
)

REASON_NOT_DRAWN = (
    ('collection_failed', 'Tried, but unable to obtain sample from patient'),
    ('absent', 'Patient did not attend visit'),
    ('refused', 'Patient refused'),
    ('no_supplies', 'No supplies'),
    (OTHER, 'Other'),
    (NOT_APPLICABLE, 'Not Applicable'))

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
    ('receiving_emotional_care', 'Already receiving emotional care'),
    ('declined', 'Declined'),
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

RELATION_TO_INDIVIDUAL = (
    ('partner', 'Partner'),
    ('child', 'Child'),
    ('mother', 'Mother'),
    ('father', 'Father'),
    ('sibling', 'Sibling'),
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
    ('1',
     'Loss of appetite but eating without staff encouragement. Heavy feelings in abdomen.'),
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

TB_SCREENING_LOCATION = (
    ('antenatal_visit', 'Antenatal Visit'),
    ('idcc', 'IDCC'),
    ('postpartum_visit', 'Postpartum visit'),
    ('hospital', 'Hospital'),
    (OTHER, 'Other (specify)'),
)

TB_DRUGS_FREQ = (
    ('4_drugs', '4 drugs'),
    ('more_than_4', 'More than 4 drugs'),
    (UNKNOWN, 'Unknown'),
    (DWTA, 'Prefer not to answer'),
)

TB_TYPE = (
    ('pulmonary', 'Pulmonary'),
    ('extra_pulmonary', 'Extra-pulmonary'),
    (UNKNOWN, 'Unknown'),
    (DWTA, 'Prefer not to answer')
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

UNSUCCESSFUL_VISIT = (
    ('no_one_was_home', 'No one was home'),
    ('location_no_longer_used', 'Previous BHP participant no longer uses this location'),
    (OTHER, 'Other'),
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

WEIGHT_LOSS = (
    ('0', 'No weight loss'),
    ('1', 'Probable weight loss associated with present illness.'),
    ('2', 'Definite (according to patient) weight loss.'),
    ('3', 'Not assessed.')
)

WHERE_SCREENED = (
    ('antenatal_visit', 'Antenatal visit'),
    ('idcc', 'IDCC'),
    ('postpartum_visit', 'Postpartum visit'),
    ('hospital', 'Hospital '),
    (OTHER, 'Other '))

WORK_INTERESTS = (
    ('0', 'No difficulty'),
    ('1', ('Thoughts and feelings of incapacity, fatigue or weakness related to'
           ' activities, work or hobbies.')),
    ('2', ('Loss of interest in activity, hobbies or work – either directly '
           'reported by the patient or indirect in listlessness, indecision and vacillations')),
    ('3', 'Decrease in actual time spent in activities or decrease in productivity'),
    ('4', ('Stopped working because of present illness.'))
)

YES_NO_UNK_DWTA = (
    (YES, YES),
    (NO, NO),
    (UNKNOWN, 'Unknown'),
    (DWTA, 'Prefer not to answer'),)

YES_NO_UNABLE_DET = (
    (YES, YES),
    (NO, NO),
    ('unable_to_determine', 'Unable to determine'),)

YES_NO_UNK_NA = (
    (YES, YES),
    (NO, NO),
    (UNKNOWN, 'Unknown'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

COUGH_DURATION = (
    ('=< 1 week', '=< 1 week'),
    ('=1-2 week', '=1-2 week'),
    ('=>2 week', '=>2 week'),
    (DWTA, 'Prefer not to answer'),

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

'''
Choices for the covid form
'''

YES_NO_COVID_FORM = (
    (YES, 'Yes'),
    (NO, 'No'),
    ('tried_but_could_not_get_tested', 'Tried, but could not get tested '),
    (UNKNOWN, 'Unknown'),

)

MONTH_YEAR = (
    ('month', 'Month'),
    ('year', 'Year')
)

COVID_RESULTS = (
    ('negative', 'Negative'),
    ('positive', 'Positive'),
    (UNKNOWN, 'Unknown'),
    (DWTA, 'Prefer not to answer'),
    ('indeterminate', 'Indeterminate'),
)

TESTING_REASONS = (
    ('pre-traveling_screening ', 'Pre-Traveling screening'),
    ('routine_testing ', 'Routine testing (experiencing symptoms)'),
    ('contact_tracing', 'Contact tracing'),
    ('asymptomatic_testing', 'Routine Testing(Asymptomatic)'),
    (OTHER, 'Other')
)

POS_NEG_PENDING_UNKNOWN = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (PENDING, 'Pending'),
    (UNKNOWN, 'Unknown'),
)

POS_NEG_IND_UNKNOWN = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (PENDING, 'Pending'),
    (IND, 'Pending'),
    (UNKNOWN, 'Unknown'),
)


ISOLATION_LOCATION = (
    ('home', 'Home'),
    ('hospital', 'Hospital'),
    ('clinic', 'Clinic'),
    (OTHER, 'Other'),
)

YES_NO_PARTIALLY = (
    (YES, 'Yes'),
    (NO, 'No'),
    ('partially_jab', 'Partially'),

)

VACCINATION_TYPE = (
    ('astrazeneca', 'AstraZeneca'),
    ('sinovac', 'Sinovac'),
    ('pfizer', 'Pfizer'),
    ('johnson_and_johnson', 'Johnson & Johnson '),
    ('moderna', 'Moderna'),
    (OTHER, 'Other')
)

REASONS_NOT_PARTICIPATE = (
    ('not_interested_in_participating', 'Not interested in participating'),
    ('busy_during_the_suggested_times ', 'Busy during the suggested times'),
    ('out_of_town_during_the_suggested_times',
     'Out of town during the suggested times'),
    ('not_available_during_the_suggested_times',
     'Not available during the suggested times'),
    ('prefers_not_to_say_why_unwilling', 'Prefers not to say why unwilling'),
    ('caregiver_is_busy_and_does_not_want_to_participate ',
     'Caregiver is busy and does not want to participate '),
    ('caregiver_does_not_live_in_study_area',
     'Caregiver does not live in study area'),
    ('caregiver_is_not_willing_to_disclose_status_to_their_child',
     'Caregiver is not willing to disclose status to their child'),
    ('caregiver_does_not_want_to_join_another_study',
     'Caregiver does not want to join another study  '),
    ('caregiver_has_work_constraints  ', 'Caregiver has work constraints  '),
    ('caregiver_has_fears_of_joining_study_or_traveling_during_covid ',
     'Caregiver has fears of joining study/traveling during COVID '),
    ('caregivers_partner_does_not_want_or_allow_them_to_participate',
     'Caregiver’s partner does not want/allow them to participate'),
    ('caregiver_has_many_other_doctor_appointments',
     'Caregiver has many other doctor appointments'),
    ('caregiver_fears_stigmatization', 'Caregiver fears stigmatization'),
    ('child_is_busy_and_does_not_want_to_participate',
     'Child is busy and does not want to participate'),
    ('child_is_not_interested_in_joining_study',
     'Child is not interested in joining study'),
    ('child_does_not_live_in_study_area', 'Child does not live in study area'),
    ('child_has_fears_of_joining_study_or_traveling_during_covid',
     'Child has fears of joining study/traveling during COVID'),
    ('child_has_many_other_doctor_appointments',
     'Child has many other doctor appointments'),
    ('caregiver_fears_stigmatization', 'Caregiver fears stigmatization'),
    ('child_is_late_has_passed_away', 'Child is late (has passed away)'),
    ('biological_mother_is_late_has_passed_away, and caregiver is unwilling',
     'Biological mother is late (has passed away), and caregiver is unwilling'),
    ('child_is_unwilling_and_prefers_not_to_say_why',
     'Child is unwilling and prefers not to say why'),
    (OTHER, 'Other'),
    (NOT_APPLICABLE, 'Not Applicable')
)

GENDER_OTHER = (
    (MALE, _('Male')),
    (FEMALE, _('Female')),
    (OTHER, _('Other')),
)

HIV_STATUS = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (UNKNOWN, 'Unknown'),)

FEEDING_HIV_STATUS = (
    (YES, 'Yes'),
    (NO, 'No'),
    ('rather_not_answer', 'Rather not answer'))

HIV_STATUS_AWARE = (
    ('during_preg', 'Later during pregnancy'),
    ('before_delivery', 'At/shortly after delivery'),
    ('after_delivery', 'After Delivery'),)

ON_HIV_STATUS_AWARE = (
    (YES, 'Yes'),
    (NO, 'No'),
    ('no_plan', 'I did not make a feeding plan before I was aware of my HIV status'),)

HIV_STATUS_KNOWN_BY = (
    ('no_one', '0 persons in my household'),
    ('one_person', '1 persons in my household'),
    ('two_or_more', '≥2 persons in my household'),)

HIV_STATUS_KNOWN_BY_FATHER = (
    (YES, 'Yes'),
    (NO, 'No'),)

ADVICED = (
    (YES, 'Yes'),
    (NO, 'No'),
    ('do_not_remember', 'Do not remember'),)

AGREE_DISAGREE = (
    ('strongly_disagree', 'Strongly disagree'),
    ('disagree', 'Disagree'),
    ('neutral', 'Neither agree or disagree'),
    ('agree', 'Agree'),
    ('strongly_agree', 'Strongly agree'),)

BREASTFEEDING_DURATION = (
    ('less_than_six_months', '<6 months'),
    ('six_months', '6 months'),
    ('six_to_twelve_months', '6-12 months'),
    ('twelve_months', '12 months'),
    ('greater_than_twelve_months', '>12 months'),
    ('do_not_know', "I don’t know"),)

FEEDING_ADVICE = (
    ('Formula_feeding', 'Formula feeding'),
    (BREASTFEED_ONLY, 'Breast feed'),
    ('mixed_feeding', 'Mixed formula and breast feed'),
    (NOT_APPLICABLE, 'Not applicable'),)

AFTER_BIRTH_OPINION = (
    ('continued_breastfeeding', 'Wanted to continue breastfeeding and was able to do so'),
    ('unable_to_breastfeed', 'Wanted to continue breastfeeding but was unable to do so'),
    ('did_not_want_to_breastfeed', 'No longer wanted to breastfeed'),
    ('told_not_to_breastfeed_before', 'Was told not to breastfeed before/at delivery'),
    ('did_not_want_to_breastfeed_before',
     'Did not want to breastfeed even before this baby was born '),
    (NONE, 'None of the above'),
    (OTHER, 'Other(specify)'))

FEEDING_INFLUENCE = (
    (YES, 'Yes'),
    (NO, 'No'),
    (NOT_APPLICABLE, 'Not Applicable'),)

RETURNED_TO_WORK = (
    ('less_than_one_month_after_delivery', '<1 month after delivery'),
    ('one_to_three_months_after_delivery', '1-3 months after delivery'),
    ('four_months_or_greater', '≥4 months after delivery'),
    (NOT_APPLICABLE, 'Not Applicable'),)

FEEDING_AFTER_SIX_MONTHS = (
    (YES, 'Yes'),
    (NO, 'No'),
    ('do_not_remember', 'Unsure/Do not remember'),)

TRAINEE_OUTCOME = (
    ('strongly_disagree', 'Strongly disagree'),
    ('disagree', 'Disagree'),
    ('neutral', 'Neither agree or disagree'),
    ('agree', 'Agree'),
    ('strongly_agree', 'Strongly agree'),)

REASONS_NOT_PARTICIPATING = (
    ('still_thinking ', 'Still thinking '),
    ('prefers_not_to_Say', 'Prefers not to say why unwilling '),
    ('outside_study_area', 'Confinement outside study area'),
    ('too_many_dr_apps', 'Has too many Doctors’ appointment '),
    ('family_refuse', 'Family member/ partner declines participant’s enrolment'),
    ('not_interested', 'Not Interested in participating'),
    (OTHER, 'Other'),)

REASONS_UNWILLING_ADOL = (
    ('unable_to_provide_consent ', 'Caregiver unavailable to provide consent'),
    ('refuses_to_provide_consent', 'Caregiver refuses to provide consent'),
    ('unwilling_to_blood_draw_adolescent',
     'Unwilling for adolescent to do blood draw'),
    ('cannot_come_to_clinic', 'Cannot physically come to clinic'),
    ('not_interested', 'Not Interested in participating'),
    (OTHER, 'Other (Specify'),)

YES_NO_PNTA_UNKNOWN = (
    (YES, YES),
    (NO, NO),
    (PNTA, _('Prefer not to answer')),
    (UNKNOWN, 'Unknown'),
)

YES_NO_DN_PNTA = (
    (YES, YES),
    (NO, NO),
    ('dont_know', 'I do not know'),
    (PNTA, _('Prefer not to answer')),
)

EMO_SUPPORT_DECLINE = (
    ('not_yet_sought_clinic', 'I have not yet sought the clinic'),
    ('could_not_get_clinic_booking',
     'I went to the clinic but could not get a booking'),
    ('partner_dnw_me_to_attend', 'My partner does not want me to attend'),
    ('family_dnw_me_to_attend', 'My family does not want me to attend'),
    ('no_longer_need_support', 'I felt I no longer need emotional support'),
    ('work_constraints', 'Work constraints'),
    ('no_transport_fare', 'I did not have transport fare'),
    (OTHER, 'Other, specify'),)

NO_EMO_SUPPORT_REASON = (
    ('professional_not_around', 'Social worker/ Psychologist/ Psychiatrist not around'),
    ('clinic_long_queue', 'Long queue at the clinic'),
    ('told_idn_emo_support', 'I was told I don’t need emotional support'),
    ('was_treated_well_at_facility',
     'I was not treated well at the health facility and I had to leave'),
    ('changed_mind', 'Changed mind and returned home'),
    (OTHER, 'Other, specify'),)

EMO_HEALTH_IMPROVED = (
    ('difficult_to_tell', 'Difficult to tell because I am still receiving emotional support'),
    ('mood_has_improved', 'My mood has improved'),
    ('not_able_to_relax', 'I am now able to relax'),
    ('relationship_with_other_improved',
     'My relationship with other people/family members/partner has improved'),
    ('able_to_manage_emotions',
     'I am now able to manage my thoughts, feelings and emotions'),
    ('accepted_medical_condition',
     'I have accepted my medical condition and I have learnt to stay positive'),
    ('accepted_loved_one_loss', 'I have now accepted the loss of my loved one'),
    ('feeling_fine', 'Emotional support received and feeling fine now'),
    ('no_longer_suicidal', 'I am no longer suicidal'),
    ('defaulted', 'Gave up and defaulted (No difference)'),
    (OTHER, 'Other, specify'))

PERCEIVE_COUNSELOR = (
    ('approachable', 'Approachable'),
    ('respectful', 'Respectful'),
    ('trustworthy', 'Trustworthy'),
    ('patient', 'Patient'),
    ('demeaning', 'Demeaning'),
    ('judgmental', 'Judgmental'),
    ('discriminatory', 'Discriminatory'),
    (PNTA, _('Prefer not to answer')),
    (OTHER, 'Other, specify'))

YES_NO_PNTA = (
    (YES, YES),
    (NO, NO),
    (PNTA, _('Prefer not to answer')),
)

YES_NO_PNTA_DNK = (
    (YES, YES),
    (NO, NO),
    (PNTA, _('Prefer not to answer')),
    (DONT_KNOW, 'Do not know')
)

YES_NO_PNTA_NA = (
    (YES, YES),
    (NO, NO),
    (PNTA, _('Prefer not to answer')),
    (NOT_APPLICABLE, 'Not Applicable')

)

HIV_STATUS_DISCUSSION = (
    ('very_difficult', 'Very Difficult'),
    ('difficult', 'Difficult'),
    ('neutral', 'Neutral'),
    ('easy', 'Easy'),
    ('very_easy', 'Very Easy'),
    (PNTA, 'Prefer not to answer'),
    (NOT_APPLICABLE, 'Not Applicable')
)

INTERVIEW_LOCATIONS = (
    ('FLOURISH_clinic', 'FLOURISH clinic'),
    ('BHP_site', 'BHP site'),
    ('part_home', 'Participant home'),
    (OTHER, 'Other'))

INTERVIEW_LANGUAGE = (
    ('setswana', 'Setswana'),
    ('english', 'English'),
    ('both', 'Both'))

PARTNERS_SUPPORT = (
    ('very_supportive', 'Very Supportive'),
    ('supportive', 'Supportive'),
    ('neutral', 'Neutral'),
    ('unsupportive', 'Unsupportive'),
    ('very_unsupportive', 'Very Unsupportive'),
    (PNTA, 'Prefer not to answer'),
)

CHOICE_FREQUENCY = (
    (PNTA, 'Prefer not to answer'),
    ('never', 'Never'),
    ('rarely', 'Rarely'),
    ('occasionally', 'Occasionally'),
    ('more_often', 'More often than not'),
    ('most_of_the_time', 'Most of the time'),
    ('all_the_time', 'All the time'),
)

HAPPINESS_CHOICES = (
    ('perfect', 'Perfect'),
    ('extremely_happy', 'Extremely Happy'),
    ('very_happy', 'Very Happy'),
    ('happy', 'Happy'),
    ('little_happy', 'A little happy'),
    ('little_unhappy', 'A little unhappy'),
    ('fairly_unhappy', 'Fairly unhappy'),
    (PNTA, 'Prefer not to answer')
)

FUTURE_OF_RELATIONSHIP = (
    ('do_anything',
     'I want desperately for the partnership to succeed and will do anything to see that it does'),
    ('do_what_I_can',
     'I want for my partnership to succeed and will do what I can to see that it does'),
    ('cannot_do_much',
     'It would be nice if my partnership succeeded, but I can’t do too much more than I do now'),
    ('refuse_to_do_more',
     'It would be nice if my partnership succeeded, but I refuse to do more'),
    ('nothing_more',
     'My partnership can never succeed and there is nothing more I can do'),
    (PNTA, 'Prefer not to answer')
)

FATHER_VISITS = (
    ('every_day', 'Every day'),
    ('every_week_weekend', "Every week/weekend"),
    ('every_month', "Every month"),
    ('every_couple_of_months', 'Every couple of months'),
    ('every_year', 'Every year'),
    (NEVER, 'Never'),
    ('do_not_know', 'I don’t know'),
    (PNTA, 'Prefer not to answer'),
    (NOT_APPLICABLE, 'Not Applicable')

)

FATHERS_FINANCIAL_SUPPORT = (
    ('not_supportive', 'Not supportive'),
    ('supportive', 'Supportive'),
    ('very_supportive', 'Very supportive'),
    (PNTA, 'Prefer not to answer'),
    (DONT_KNOW, 'I don’t know'),
    (NOT_APPLICABLE, 'Not Applicable')

)

HOUSEHOLD_MEMBER = (
    ('mother', 'Mother'),
    ('father', 'Father'),
    ('other', 'Other'),
    ('no_one', 'No-one'),
    (PNTA, 'Prefer not to answer'),
)

VISIT_NUMBER = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6 or more')
)

CARE_TYPE = (
    ('antenatal visit', 'Antenatal visit'),
    ('IDCC', 'IDCC'),
    ('postpartum_visit', 'Postpartum visit'),
    ('hospital', 'Hospital'),
    ('OPD', 'OPD'),
    (OTHER, 'Other')
)

EVAL_LOCATION = (
    ('bontleng', 'Bontleng'),
    ('julia_molefe', 'Julia Molefe'),
    ('phase_2', 'Phase 2'),
    ('BH1', 'BH1'),
    ('BH2', 'BH2'),
    ('BH3', 'BH3'),
    ('nkoyaphiri', 'Nkoyaphiri'),
    ('lesirane', 'Lesirane'),
    ('mogoditshane', 'Mogoditshane'),
    ('old_naledi', 'Old Naledi'),
    ('g_west', 'G-West'),
    ('sebele', 'Sebele'),
    (OTHER, 'Other, specify')
)

PREFERENCE_CHOICES = (
    ('one_on_one', 'One-on-one interview'),
    ('group', 'Group discussion'),
    ('either', 'Either one-one or group discussion'),
    ('unsure', 'Unsure'),
    ('not_participate', 'Prefer not to participate'),
)

DISCUSSION_PREF_CHOICES = (
    ('one_on_one', 'One-on-one interview'),
    ('group', 'Group discussion'),
    ('either', 'Either one-one or group discussion'),
    ('unsure', 'Unsure'),
)

HIV_GROUP_CHOICES = (
    ('same_status', 'Members who have the same HIV status as you'),
    ('mixed_status', 'A group where some persons are living with HIV and some are not'),
    ('no_preference', 'I have no preference'),
    ('unsure', 'Unsure'),
)

YES_NO_TBD = (
    (YES, YES),
    (NO, NO),
    ('TBD', 'I will think about it'),
)


HIV_TESTING_REFUSAL_REASON = (
    ('no_apparent_reason', 'No apparent reason'),
    ('time_constraints', 'Time constraints'),
    ('busy_schedule_at_work', 'Busy schedule at work'),
    ('I_did_not_know_it_was_uncessary', 'I did not know it was necessary'),
    ('test_kits_out_of_stock', 'Test kits out of stock at local clinic '),
    ('not_ready', 'Not ready for testing'),
    (OTHER, 'Other'),
)
