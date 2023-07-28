from edc_constants.choices import YES, NO
from edc_constants.constants import (CONTINUOUS, RESTARTED, OTHER, STOPPED,
                                     NOT_APPLICABLE, NEW, NEG, POS, IND, PENDING)

from .constants import (LIVE, STILL_BIRTH, MISSED, NO_SAMPLE_COLLECTED,
                        NO_SAMPLE_TUBES, MACHINE_NOT_WORKING, FORGOT)

LIVE_STILL_BIRTH = (
    (LIVE, 'live birth'),
    (STILL_BIRTH, 'still birth')
)

YES_NO_DNT_DWTA = (
    (YES, YES),
    (NO, NO),
    ('Dont know right now', 'I do not know right now'),
    ('DWTA', 'Don\'t want to answer'))

YES_NO_NO_PARTNER_DWTA = (
    (YES, YES),
    (NO, NO),
    ('no_partner', 'I do not currently have a partner'),
    ('DWTA', 'Don\'t want to answer'))

NEXT_CHILD_PLAN = (
    ('within 2years', 'Within the next 2 years'),
    ('between 2-5years from now', 'From 2 years to 5 years from now'),
    ('More than 5years from now', 'More than 5 years from now'),
    ('Dont know right now', 'I do not know right now'),
    ('DWTA', 'Don\'t want to answer'))

RECRUIT_SOURCE = (
    ('ANC clinic staff', 'ANC clinic staff'),
    ('BHP recruiter/clinician', 'BHP recruiter/clinician'),
    (OTHER, 'Other, specify'),
)

RECRUIT_CLINIC = (
    ('Prior', 'Prior BHP Study'),
    ('PMH', 'Gaborone(PMH)'),
    ('G.West Clinic', 'G.West Clinic'),
    ('BH3 Clinic', 'BH3 Clinic'),
    ('Ext2', 'Extension 2 Clinic'),
    ('Nkoyaphiri', 'Nkoyaphiri Clinic'),
    ('Lesirane', 'Lesirane Clinic'),
    ('Old Naledi', 'Old Naledi'),
    ('Mafitlhakgosi', 'Mafitlhakgosi'),
    ('Schools', 'Schools'),
    (OTHER, 'Other health facilities not associated with study site'),
)

DELIVERY_HEALTH_FACILITY = (
    ('PMH', 'Gaborone(PMH)'),
    ('G.West Clinic', 'G.West Clinic'),
    ('BH3 Clinic', 'BH3 Clinic'),
    ('Lesirane', 'Lesirane Clinic'),
    ('Old Naledi', 'Old Naledi'),
    ('Mafitlhakgosi', 'Mafitlhakgosi'),
    (OTHER, 'Other health facilities not associated with study site'),
)

PRIOR_PREG_ART_STATUS = (
    (CONTINUOUS,
     'Received continuous ART from the time she started'),
    (RESTARTED,
     'Had treatment interruption but restarted ART prior to this pregnancy'),
    (STOPPED,
     'Had treatment interruption and never restarted ART '
     'prior to this pregnancy'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

CSECTION_REASON = (
    (NOT_APPLICABLE, 'Not Applicable'),
    ('arrest', 'Arrest'),
    ('non-reassuring fetal fetal heart rate',
     'Non-reassuring fetal heart rate'),
    ('malpresentation/breeech fetus', 'Malpresentation/breech fetus'),
    ('interruption of hiv transmission', 'Interruption of HIV transmission'),
    ('failure to progress/descend', 'Failue to progress/descend'),
    ('fetal anomaly', 'Fetal anomaly'),
    (OTHER, 'Other reason for csection not listed above.')
)

DELIVERY_MODE = (
    ('spontaneous vaginal', 'spontaneous vaginal'),
    ('vaginal forceps', 'vaginal forceps'),
    ('elective c-section', 'elective C-section'),
    ('emergent c-section', 'emrgent C-section'),
    (OTHER, 'Other delivery mode not listed above')
)

MARITAL_STATUS = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Cohabiting', 'Cohabiting'),
    ('Widowed', 'Widowed'),
    ('Divorced', 'Divorced'),
    (OTHER, 'Other, specify'))

ETHNICITY = (
    ('Black African', 'Black African'),
    ('Caucasian', 'Caucasian'),
    ('Asian', 'Asian'),
    (OTHER, 'Other, specify'))

HIGHEST_EDUCATION = (
    ('None', 'None'),
    ('Primary', 'Primary'),
    ('Junior Secondary', 'Junior Secondary'),
    ('Senior Secondary', 'Senior Secondary'),
    ('Tertiary', 'Tertiary'))

CURRENT_OCCUPATION = (
    ('Housewife', 'Housewife'),
    ('Salaried (government)', 'Salaried (government)'),
    ('Salaried (private, not including domestic work)',
     'Salaried (private, not including domestic work)'),
    ('Domestic work (paid)', 'Domestic work (paid)'),
    ('Self-employed', 'Self-employed'),
    ('Student', 'Student'),
    ('Unemployed', 'Unemployed'),
    (OTHER, 'Other, specify'))

MONEY_PROVIDER = (
    ('You', 'You'),
    ('Partner/husband', 'Partner/husband'),
    ('Mother', 'Mother'),
    ('Father', 'Father'),
    ('Sister', 'Sister'),
    ('Brother', 'Brother'),
    ('Aunt', 'Aunt'),
    ('Uncle', 'Uncle'),
    ('Grandmother', 'Grandmother'),
    ('Grandfather', 'Grandfather'),
    ('Mother-in-law or Father-in-law', 'Mother-in-law or Father-in-law'),
    ('Friend', 'Friend'),
    ('Work collegues', 'Work collegues'),
    ('Unsure', 'Unsure'),
    (OTHER, 'Other, specify'))

MONEY_EARNED = (
    ('None', 'None'),
    ('<P200 per month / <P47 per week', '<P200 per month / <P47 per week'),
    ('P200-500 per month / P47-116 per week',
     'P200-500 per month / P47-116 per week'),
    ('P501-1000 per month / P117 - 231 per week',
     'P501-1000 per month / P117 - 231 per week'),
    ('P1001-5000 per month / P212 - 1157 per week',
     'P1001-5000 per month / P212 - 1157 per week'),
    ('>P5000 per month / >P1157 per week',
     '>P5000 per month / >P1157 per week'),
    ('Unsure', 'Unsure'),
    (OTHER, 'Other, specify'))

WATER_SOURCE = (
    ('Piped directly into the house', 'Piped directly into the house'),
    ('Tap in the yard', 'Tap in the yard'),
    ('Communal standpipe', 'Communal standpipe'),
    (OTHER, 'Other water source (stream, borehole, rainwater, etc)'),)

COOKING_METHOD = (
    ('Gas or electric stove', 'Gas or electric stove'),
    ('Paraffin stove', 'Paraffin stove'),
    ('Wood-burning stove or open fire', 'Wood-burning stove or open fire'),
    ('No regular means of heating', 'No regular means of heating'),)

TOILET_FACILITY = (
    ('Indoor toilet', 'Indoor toilet'),
    ('Private latrine for your house/compound',
     'Private latrine for your house/compound'),
    ('Shared latrine with other compounds',
     'Shared latrine with other compounds'),
    ('No latrine facilities', 'No latrine facilities'),
    (OTHER, 'Other, specify'),)

HOUSE_TYPE = (
    ('Formal:Tin-roofed, concrete walls',
     'Formal: Tin-roofed, concrete walls'),
    ('Informal: Mud-walled or thatched', 'Informal: Mud-walled or thatched'),
    ('Mixed formal/informal', 'Mixed formal/informal'),
    ('Shack/Mokhukhu', 'Shack/Mokhukhu'),)

KNOW_HIV_STATUS = (
    ('Nobody', 'Nobody'),
    ('1 person', '1 person'),
    ('2-5 people', '2-5 people'),
    ('6-10 people', '6-10 people'),
    ('More than 10 people', 'More than 10 people'),
    ('dont know', 'I do not know'),)

DX = (
    ('Pneumonia suspected, no CXR or microbiologic confirmation',
     'Pneumonia suspected, no CXR or microbiologic confirmation'),
    ('Pneumonia, CXR confirmed, no bacterial pathogen',
     'Pneumonia, CXR confirmed, no bacterial pathogen'),
    ('Pneumonia, CXR confirmed, bacterial pathogen isolated '
     '(specify pathogen)',
     'Pneumonia, CXR confirmed, bacterial pathogen isolated '
     '(specify pathogen)'),
    ('Pulmonary TB, suspected(no CXR or microbiologic confirmation)',
     'Pulmonary TB, suspected(no CXR or microbiologic confirmation)'),
    ('Pulmonary TB, CXR-confirmed (no microbiologic confirmation)',
     'Pulmonary TB, CXR-confirmed (no microbiologic confirmation)'),
    ('Pulmonary TB, smear and/or culture positive',
     'Pulmonary TB, smear and/or culture positive'),
    ('Extrapulmonary TB,suspected (no CXR or microbiologic confirmation) ',
     'Extrapulmonary TB,suspected (no CXR or microbiologic confirmation) '),
    ('Extrapulmonary TB, smear and/or culture positive',
     'Extrapulmonary TB, smear and/or culture positive'),
    (('Acute diarrheal illness (bloody diarrhean OR increase of at least '
      '7 stools per day '
      'OR life threatening for less than 14 days) '),
     ('Acute diarrheal illness (bloody diarrhean OR increase of at least '
      '7 stools per day OR '
      'life threatening for less than 14 days)')),
    ('Chronic diarrheal illness (as above but for 14 days or longer) ',
     'Chronic diarrheal illness (as above but for 14 days or longer) '),
    ('Acute Hepatitis in this pregnancy: Drug related ',
     'Acute Hepatitis in this pregnancy: Drug related '),
    ('Acute Hepatitis in this pregnancy:Traditional medication related',
     'Acute Hepatitis in this pregnancy:Traditional medication related'),
    ('Acute Hepatitis in this pregnancy:Fatty liver disease',
     'Acute Hepatitis in this pregnancy:Fatty liver disease'),
    ('Acute Hepatitis in this pregnancy:Hepatitis A',
     'Acute Hepatitis in this pregnancy:Hepatitis A'),
    ('Acute Hepatitis in this pregnancy:Hepatitis B ',
     'Acute Hepatitis in this pregnancy:Hepatitis B'),
    ('Acute Hepatitis in this pregnancy:Alcoholic',
     'Acute Hepatitis in this pregnancy:Alcoholic'),
    ('Acute Hepatitis in this pregnancy:Other/Unkown',
     'Acute Hepatitis in this pregnancy:Other/Unkown'),
    ('Sepsis, unspecified', 'Sepsis, unspecified'),
    ('Sepsis, pathogen specified', 'Sepsis, pathogen specified'),
    ('Meningitis, unspecified', 'Meningitis, unspecified'),
    ('Meningitis, pathogen specified', 'Meningitis, pathogen specified'),
    ('Appendicitis', 'Appendicitis'),
    ('Cholecystitis/cholanangitis', 'Cholecystitis/cholanangitis'),
    ('Pancreatitis', 'Pancreatitis'),
    ('Acute Renal failure',
     'Acute Renal failure (Record highest creatinine level if tested '
     'outside of the study)'),
    ('Anemia',
     'Anemia (Only report grade 3 or 4 anemia based on the lab value '
     'drawn outside the study)'),
    ('Pregnancy/peripartum cardiomyopathy or CHF ',
     'Pregnancy/peripartum cardiomyopathy or CHF '),
    ('Drug rash on HAART', 'Drug rash on HAART'),
    ('Trauma/Accident', 'Trauma/Accident'),
    ('Other serious (grade 3 or 4) infection, specify',
     'Other serious (grade 3 or 4) infection(not listed above), specify'),
    ('Other serious (grade 3 or 4) non-infectious diagnosis, specify',
     'Other serious (grade 3 or 4) non-infectious diagnosis(not listed '
     'above), specify'),
)

REASON_FOR_HAART = (
    ('maternal masa',
     'HAART for maternal treatment (qualifies by Botswana guidelines)'),
    ('pmtct bf', 'HAART for PMTCT while breastfeeding'),
    ('pp arv tail', 'Brief postpartum antiretroviral "tail"'),
    ('unsure', 'Unsure'),
    (OTHER, 'OTHER'),
    (NOT_APPLICABLE, 'Not applicable'))

# haart modification
ARV_DRUG_LIST = (
    ('Nevirapine', 'NVP'),
    ('Kaletra', 'KAL'),
    ('Aluvia', 'ALU'),
    ('Truvada', 'TRV'),
    ('Emtricitabine', 'FTC'),
    ('Tenoforvir', 'TDF',),
    ('Zidovudine', 'AZT'),
    ('Lamivudine', '3TC'),
    ('Efavirenz', 'EFV'),
    ('Didanosine', 'DDI'),
    ('Stavudine', 'D4T'),
    ('Nelfinavir', 'NFV'),
    ('Abacavir', 'ABC'),
    ('Combivir', 'CBV'),
    ('Ritonavir', 'RTV'),
    ('Trizivir', 'TZV'),
    ('Raltegravir', 'RAL'),
    ('Saquinavir,soft gel capsule', 'FOR'),
    ('Saquinavir,hard capsule', 'INV'),
    ('Kaletra or Aluvia', 'KAL or ALU'),
    ('Atripla', 'ATR'),
    ('Dolutegravir', 'DTG'),
    ('HAART,unknown', 'HAART,unknown'),
)

DOSE_STATUS = (
    (NEW, 'New'),
    ('Permanently discontinued', 'Permanently discontinued'),
    ('Temporarily held', 'Temporarily held'),
    ('Dose modified', 'Dose modified'),
    ('Resumed', 'Resumed'),
    ('Not initiated', 'Not initiated'),
)

ARV_MODIFICATION_REASON = (
    ('Initial dose', 'Initial dose'),
    ('Never started', 'Never started'),
    ('Toxicity decreased_resolved', 'Toxicity decreased/resolved'),
    ('Completed PMTCT intervention', 'Completed PMTCT intervention'),
    ('Completed postpartum tail', 'Completed postpartum "tail"'),
    ('Scheduled dose increase', 'Scheduled dose increase'),
    ('Confirmed infant HIV infection, ending study drug',
     'Confirmed infant HIV infection, ending study drug'),
    ('completed protocol',
     'Completion of protocol-required period of study treatment'),
    ('HAART not available', 'HAART not available'),
    ('Anemia', 'Anemia'),
    ('Bleeding', 'Bleeding'),
    ('CNS symptoms', 'CNS symptoms (sleep, psych, etc)'),
    ('Diarrhea', 'Diarrhea'),
    ('Fatigue', 'Fatigue'),
    ('Headache', 'Headache'),
    ('Hepatotoxicity', 'Hepatotoxicity'),
    ('Nausea', 'Nausea'),
    ('Neutropenia', 'Neutropenia'),
    ('Thrombocytopenia', 'Thrombocytopenia'),
    ('Vomiting', 'Vomiting'),
    ('Rash', 'Rash'),
    ('Rash resolved', 'Rash resolved'),
    ('Neuropathy', 'Neuropathy'),
    ('Hypersensitivity_allergic reaction',
     'Hypersensitivity / allergic reaction'),
    ('Pancreatitis', 'Pancreatitis'),
    ('Lactic Acidiosis', 'Lactic Acidiosis'),
    ('Pancytopenia', 'Pancytopenia'),
    ('Virologic failure', 'Virologic failure'),
    ('Immunologic failure', 'Immunologic failure(CD4)'),
    ('Clinical failure', 'Clinical failure'),
    ('Clinician request',
     'Clinician request, other reason (including convenience)'),
    ('Subject request',
     'Subject request, other reason (including convenience)'),
    ('Non-adherence with clinic visits', 'Non-adherence with clinic visits'),
    ('Non-adherence with ARVs', 'Non-adherence with ARVs'),
    ('Death', 'Death'),
    (OTHER, 'Other'),
)

REASON_UNSEEN_AT_CLINIC = (
    ('not_tried', 'I have not yet sought the clinic'),
    ('no_booking', 'I went to the clinic but could not get a booking'),
    ('in_confinement', 'I am observing confinement'),
    ('not_sexually_active', 'I am not sexually active right now'),
    ('no_contraception_bf',
     'I do not need contraception because I am breastfeeding'),
    ('too_far', 'The clinic is too far from my home'),
    ('partner_refused', 'My partner does not want me to attend'),
    ('mother_refused', 'My mother does not want me to attend'),
    (OTHER, 'Other'),
)

REASON_CONTRACEPTIVE_NOT_INITIATED = (
    ('no_options', 'There was not an option I preferred'),
    ('no_stock_for_preference',
     'The option I preferred was out of stock (state option if this'
     ' answer is indicated)'),
    ('not_sexually_active', 'I am not currently sexually active'),
    ('disrespected', 'I felt disrespected by the SRH clinic'),
    ('no_contraception_bf',
     'I was told that because I am breastfeeding, I do not need a '
     'contraceptive metod'),
    ('partner_refused',
     'My current partner does not want me to use a contraceptive method'),
    ('was not attended by a clinician',
     'I was not attended by a clinician when I went to the SRH clinic'),
    (OTHER, 'Other'),
)

SITE = (
    ('Gaborone', 'Gaborone'),
)

PAP_SMEAR = (
    (YES, YES),
    (NO, NO),
    ('never_had_pap_smear', 'I have never had a Pap smear'),
    ('DWTA', 'Don\'t want to answer')
)

NORMAL_ABNORMAL_DWTA = (
    ('normal', 'Normal'),
    ('abnormal', 'Abnormal'),
    ('DWTA', 'Don\'t Want to Answer')
)

PAP_SMEAR_ESTIMATE = (
    ('within_last_6months', 'Within the last 6 months'),
    ('more_than_6months_within_1year',
     'More than 6 months ago but within the last year'),
    ('more_than_1year_within_2years',
     'More than one year ago but within the last two years'),
    ('more_than_1year_within_5years',
     'More than one year ago but within the last five years'),
    ('more_than_5years', 'More than five years ago')
)

INFLUENTIAL_IN_DECISION_MAKING = (
    ('independent_decision',
     'I made the decision independent of any discussions I have had.'),
    ('partner_most_influential', 'My partner was the most influential.'),
    ('mother_most_influential', 'My mother was the most influential.'),
    ('sister_most_influential', 'My sister was the most influential.'),
    ('auntie_most_influential', 'My auntie was the most influential.'),
    ('mother_in_law_most_influential',
     'My mother-in-law was the most influential'),
    ('DWTA', 'I do not wish to answer this question'),
    (NOT_APPLICABLE, 'Not Applicable'),
    (OTHER,
     'Another person was the most influential (Please type in the '
     'description of this person below)')
)

FEEDING_CHOICES = (
    ('FF', "formula"),
    ('BF', "breast"),
)

BF_DURATION = (
    ('36months', '36m'),
    ('12months', '12m'),
    ('6months', '6m'),
)

KNOW_HIV_STATUS = (
    ('Nobody', 'Nobody'),
    ('1 person', '1 person'),
    ('2-5 people', '2-5 people'),
    ('6-10 people', '6-10 people'),
    ('More than 10 people', 'More than 10 people'),
    ('dont know', 'I do not know'),
    (NOT_APPLICABLE, 'Not applicable')
)

LOWEST_CD4_KNOWN = (
    (YES, 'Yes'),
    (NO, 'No'),
    (NOT_APPLICABLE, 'Not applicable')
)

IS_DATE_ESTIMATED = (
    (NO, 'No'),
    ('Yes, estimated the Day', 'Yes, estimated the Day'),
    ('Yes, estimated Month and Day', 'Yes, estimated Month and Day'),
    ('Yes, estimated Year, Month and Day',
     'Yes, estimated Year, Month and Day'),

)

SMOKING_DRINKING_FREQUENCY = (
    ('daily', 'Daily'),
    ('once every few days', 'Once every few days'),
    ('weekly', 'Weekly'),
    ('2-3 times per month or less', '2-3 times per month or less'),
)

SIZE_CHECK = (
    ('equal', '='),
    ('less_than', '<'),
    ('greater_than', '>'),
)


SIZE_CHECK_WITHOUT_EQUAL = (
    ('less_than', '<'),
    ('greater_than', '>'),
)

POS_NEG_IND = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (IND, 'Indeterminate')
)

CALL_REASON = (
    ('follow_up', 'Follow up/Quarterly calls'),
    ('missed_visit', 'Missed visit'),
    ('scheduled_appointment', 'Confirm scheduled appointment'),
    ('follow_up_delivery', 'Follow up on delivery status'),
    ('follow_up_labs', 'Follow up on abnormal labs'),
    ('re_appointment', 'Re-appointment or reschedule'),
    (OTHER, 'Other, specify')
)

CONTACT_TYPE = (
    ('phone_call', 'Phone Call'),
    ('in_person', 'In person (Home visit)'),
    ('text_message', 'Text Message')
)

KHAT_USAGE_FREQUENCY = (
    ('daily', 'Daily'),
    ('once_every_few_weeks', 'Once every few weeks'),
    ('weekly', 'Weekly'),
    ('two_three_times_per_month', '2-3 times per month or less'))

REASONS_FOR_RESCHEDULING = (
    ('out_of_study_area', 'Temporarily out of study area'),
    ('no_transport_fares', 'Participant do not have transport fares'),
    ('schools_are_reluctant_to_release_children',
     'Schools are reluctant to release children'),
    ('Child_examinations', 'Child writing examinations or tests'),
    ('phone_not_reachable', 'Phone number(s) not reachable'),
    ('home_visit_done', 'Home visit done, successful / unsuccessful'),
    ('emergency_issues', 'Participant has work or home emergency issues'),
    ('Participant_work ', 'Participant cannot be released from work'),
    ('Participant_quarantine',
     'Participant on quarantine or Isolations due to covid-19 exposure or infection'),
    ('Participant_changed_mind',
     'Participant changed mind and asked for a re-appointments or want to withdraw / be-withdraw from participating on study '),
    ('caregiver_not_well', 'Child, mother, caregiver not well'),
    ('undisclosed_personal_reasons', 'Participant has undisclosed personal reasons'),
    ('another_appointment',
     'Participant has another appointment at local clinic/hospital scheduled on the same day'),
    (OTHER, 'Other, specify')

)

GC_DHMT_CLINICS = (
    ('bontleng', 'Bontleng'),
    ('julia_molefe', 'Julia Molefe'),
    ('phase_2', 'Phase 2'),
    ('bh2', 'BH1'),
    ('bh2', 'BH2'),
    ('bh2', 'BH3'),
    ('nkoyaphiri', 'Nkoyaphiri'),
    ('mogoditshane', 'Mogoditshane'),
    ('lesirane', 'Lesirane'),
    ('old_naledi', 'Old Naledi'),
    ('g_west', 'G-West'),
    ('sebele', 'Sebele'),
    (OTHER, 'Other, specify')
)


REASON_CD4_RESULT_UNAVAILABLE = (
    (FORGOT, 'Participant forgot and did not go for sample draw'),
    (PENDING, 'Result pending'),
    (MISSED, 'Participant missed IDCC appoitment'),
    (NO_SAMPLE_COLLECTED, 'No CD4 sample requested at last IDCC review'),
    (NO_SAMPLE_TUBES, 'No sample collection tubes at local IDCC'),
    (MACHINE_NOT_WORKING, 'Diagnostic machines not working'),
    (OTHER, 'Other'),
)

REASON_VL_RESULT_UNAVAILABLE = (
    (FORGOT, 'Participant forgot and did not go for sample draw'),
    (PENDING, 'Result pending'),
    (MISSED, 'Participant missed IDCC appoitment'),
    (NO_SAMPLE_COLLECTED, 'No VL sample requested at last IDCC review'),
    (NO_SAMPLE_TUBES, 'No sample collection tubes at local IDCC'),
    (MACHINE_NOT_WORKING, 'Diagnostic machines not working'),
    (OTHER, 'Other'),
)
