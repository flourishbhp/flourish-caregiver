from edc_constants.constants import (
    OFF_STUDY, ON_STUDY, FAILED_ELIGIBILITY, PARTICIPANT)
from edc_constants.constants import ALIVE, DEAD, NOT_APPLICABLE, OTHER, UNKNOWN
from edc_constants.constants import YES, NO, POS, NEG
from edc_visit_tracking.constants import MISSED_VISIT, COMPLETED_PROTOCOL_VISIT
from edc_visit_tracking.constants import SCHEDULED, UNSCHEDULED, LOST_VISIT

from .constants import BREASTFEED_ONLY, NEVER_STARTED, MODIFIED, TUBERCULOSIS
from .constants import NO_MODIFICATIONS, START

ANSWERS = (
    ('Accepted', 'Yes and the client accepted the signed copy of the consent'),
    ('Refused', 'Yes and the client refused the signed copy of the consent'),
    (NO, 'No')
)

STUDY_SITES = (
    ('40', 'Gaborone'),
    ('10', 'Molepolole'),
)

IDENTITY_TYPE = (
    ('country_id', 'Country ID number'),
    ('country_id_rcpt', 'Country ID receipt'),
    ('passport', 'Passport'),
    (OTHER, 'Other'),
)

ALIVE_DEAD_UNKNOWN = (
    (ALIVE, 'Alive'),
    (DEAD, 'Dead'),
    (UNKNOWN, 'Unknown'),
)

OFTEN_SOMETIMES_NEVER_TRUE = (
    ('often_true', 'Often true'),
    ('sometimes_true', 'Sometimes true'),
    ('never_true', 'Never true'),
    ('dont_know_or_refused', 'Don\'t know or refused')
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

VISIT_UNSCHEDULED_REASON = (
    ('Routine oncology', 'Routine oncology clinic visit'),
    ('Ill oncology', 'Ill oncology clinic visit'),
    ('Patient called', 'Patient called to come for visit'),
    (OTHER, 'Other, specify:'),
)

HAART_DURING_PREG = (
    ('Atripla', 'Atripla'),
    ('Truvada-Efavirenz ', 'Truvada-Efavirenz '),
    ('Tenofovir-Emtricitibine-Efavirenz', 'Tenofovir-Emtricitibine-Efavirenz'),
    ('Truvad-Lamivudine-Efavirenz', 'Truvad-Lamivudine-Efavirenz'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

PREG_DELIVERED_CHOICE = (
    ('pregnant', 'Pregnant'),
    ('delivered ', 'Delivered '),
)

BIRTH_TYPE = (
    ('vaginal ', 'vaginal'),
    ('cesarean ', 'cesarean'),
)

ARV_INTERRUPTION_REASON = (
    ('TOXICITY', 'Toxicity'),
    ('NO_DRUGS', 'No drugs available'),
    ('NO_REFILL', 'Didn\'t get to clinic for refill'),
    ('FORGOT', 'Mother forgot to take the ARVs'),
    (OTHER, 'Other'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

AZT_NVP = (
    ('AZT', 'AZT'),
    ('NVP', 'NVP'),
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

AUTOPSY_SOURCE = (
    ('mother', 'Mother of infant'),
    ('family_mem', 'Other family member'),
    ('hlth_prof', 'Health Professional who cared for the infant'),
    ('med_rec', 'Medical records'),
    (OTHER, 'Other'),
)

AUTOPSY_SIGNS = (
    ('fever', 'Fever'),
    ('poor_feeding', 'Poor feeding'),
    ('weight_loss', 'Weight loss'),
    ('weakness', 'Weakness'),
    ('stiff_neck', 'Stiff Neck'),
    ('unusual_sleepiness', 'Unusual sleepiness'),
    ('convulsions', 'Convulsions'),
    ('bleeding', 'Bleeding'),
    ('cough', 'Cough'),
    ('diffic_breathing', 'Difficulty breathing'),
    ('swollen_stomach', 'Swollen stomach'),
    ('Vomiting', 'Vomiting'),
    ('diarrhea', 'Diarrhea'),
    ('blood_pus_stool', 'Blood or pus in stool'),
    ('rash_body', 'Rash on body'),
    ('rash_mouth', 'Rash or sores in mouth'),
    ('yellow_eyes_skin', 'Yellow eyes or skin'),
    ('accident', 'Accident'),
    ('infection_genitals', 'Local infection (genitals)'),
    ('infect_other_area', 'Local infection (other than genitals'),
)

FEEDING_CHOICES = (
    (BREASTFEED_ONLY, 'Breastfeed only'),
    ('Formula feeding only', 'Formula feeding only'),
    ('Both breastfeeding and formula feeding',
     'Both breastfeeding and formula feeding'),
    ('Medical complications: Infant did not feed',
     'Medical complications: Infant did not feed'),
)

CARDIOVASCULAR_DISORDER = (
    ('None', 'None'),
    ('Truncus arteriosus', 'Truncus arteriosus'),
    ('Atrial septal defect', 'Atrial septal defect'),
    ('Ventricula septal defect', 'Ventricula septal defect'),
    ('Atrioventricular canal', 'Atrioventricular canal'),
    ('Complete transposition of the great vessels (without VSD)',
     'Complete transposition of the great vessels (without VSD)'),
    ('Complete transposition of the great vessels (with VSD)',
     'Complete transposition of the great vessels (with VSD)'),
    ('Tetralogy of Fallot', 'Tetralogy of Fallot'),
    ('Pulmonary valve stenosis or atresia',
     'Pulmonary valve stenosis or atresia'),
    ('Tricuspid valve stenosis or atresia',
     'Tricuspid valve stenosis or atresia'),
    ('Mitral valve stenosis or atresia', 'Mitral valve stenosis or atresia'),
    ('Hypoplastic left ventricle', 'Hypoplastic left ventricle'),
    ('Hypoplastic right ventricle', 'Hypoplastic right ventricle'),
    ('Congenital cardiomyopath (do not code if only isolated cardiomegaly)',
     'Congenital cardiomyopath (do not code if only isolated cardiomegaly)'),
    ('Coarclation of the aorta', 'Coarclation of the aorta'),
    ('Total anomalous pulmonary venous return',
     'Total anomalous pulmonary venous return'),
    ('Arteriovenous malformation, specify site',
     'Arteriovenous malformation, specify site'),
    ('Patent ductous arteriosus (persisting >6 weeks of age)',
     'Patent ductous arteriosus (persisting >6 weeks of age)'),
    (OTHER, 'Other cardiovascular malformation, specify'),
)

CONSENT_VERSION = (
    ('1', 'Consent version 1'),
    ('3', 'Consent version 3')
)

CLEFT_DISORDER = (
    ('None', 'None'),
    ('Cleft lip without cleft palate', 'Cleft lip without cleft palate'),
    ('Cleft palate without cleft lip', 'Cleft palate without cleft lip'),
    ('Cleft lip and palate', 'Cleft lip and palate'),
    ('Cleft uvula', 'Cleft uvula'),
)

CNS_ABNORMALITIES = (
    ('None', 'None'),
    ('Anencephaly', 'Anencephaly'),
    ('Encephaloceis', 'Encephaloceis'),
    ('Spina bifida, open', 'Spina bifida, open'),
    ('Spina bifida, closed', 'Spina bifida, closed'),
    ('Holoprosencephaly', 'Holoprosencephaly'),
    ('Isolated hydroencephaly (not associated with spina bifida)',
     'Isolated hydroencephaly (not associated with spina bifida)'),
    ('Other CNS defect, specify', 'Other CNS defect, specify'),
)

COWS_MILK = (
    ('boiled', '1. Boiled from cow'),
    ('unboiled', '2. Unboiled from cow'),
    ('store', '3. From store'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

CTX_PLACEBO_STATUS = (
    ('No modification',
     'No modifications made to CTX/Placebo since the last '
     'scheduled visit or today'),
    ('Starting CTX/Placebo today',
     'Starting CTX/Placebo today or since the last scheduled visit'),
    ('Permanently discontinued',
     'Permanently discontinued CTX/Placebo at or before last scheduled visit'),
    ('Never started', 'Never started CTX/Placebo'),
    ('Change in CTX/Placebo since the last scheduled visit or today',
     (
         'Change in CTX/Placebo since the last scheduled visit or'
         ' today (dose modification, '
         'permanent discontinuation, temporary hold, resumption /'
         ' initiation after temporary hold)')),
)

DX_INFANT = (
    ('Poor weight gain or failure to thrive',
     'Poor weight gain or failure to thrive'),
    ('Severe diarrhea or gastroenteritis',
     'Severe diarrhea or gastroenteritis'),
    ('Pneumonia, suspected (no CXR or microbiologic confirmation)',
     'Pneumonia, suspected (no CXR or microbiologic confirmation)'),
    ('Pneumonia, CXR confirmed, no bacterial pathogen',
     'Pneumonia, CXR confirmed, no bacterial pathogen'),
    ('Pneumonia, CXR confirmed, bacterial pathogen '
     'isolated (specify pathogen)',
     'Pneumonia, CXR confirmed, bacterial pathogen '
     'isolated (specify pathogen)'),
    ('Pulmonary TB, suspected(no CXR or microbiologic confirmation)',
     'Pulmonary TB, suspected(no CXR or microbiologic confirmation)'),
    ('Pulmonary TB, CXR-confirmed (no microbiologic confirmation)',
     'Pulmonary TB, CXR-confirmed (no microbiologic confirmation)'),
    ('Pulmonary TB, smear and/or culture positive',
     'Pulmonary TB, smear and/or culture positive'),
    ('Extrapulmonary TB,suspected (no CXR or microbiologic confirmation)',
     'Extrapulmonary TB,suspected (no CXR or microbiologic confirmation)'),
    ('Bronchiolitis (not bronchitis)', 'Bronchiolitis (not bronchitis)'),
    ('Hepatitis:Drug related',
     'Hepatitis:Drug related (report for Grades 2,3,4)'),
    ('Hepatitis:Traditional medication related',
     'Hepatitis:Traditional medication related'),
    ('Hepatitis:Hepatitis A', 'Hepatitis:Hepatitis A'),
    ('Hepatitis:Hepatitis B', 'Hepatitis:Hepatitis B'),
    ('Hepatitis:Other/Unknown', 'Hepatitis:Other/Unknown'),
    ('Sepsis,unspecified', 'Sepsis,unspecified'),
    ('Sepsis,pathogen specified', 'Sepsis,pathogen specified'),
    ('Meningitis,unspecified', 'Meningitis,unspecified'),
    ('Meningitis pathogen specified', 'Meningitis pathogen specified'),
    ('Otitis media', 'Otitis media'),
    ('Appendicitis', 'Appendicitis'),
    ('Cholecystitis/cholanangitis', 'Cholecystitis/cholanangitis'),
    ('Pancreatitis', 'Pancreatitis'),
    ('Acute Renal Failure',
     'Acute Renal Failure (Record highest creatinine level if creatine '
     'tested outside of the study) '),
    ('Anemia',
     'Anemia(Only report grade 3 or 4 anemia based on a lab value drawn '
     'outside the study'),
    ('Rash', 'Rash (report for Grades 2,3,4)'),
    ('Trauma/accident', 'Trauma/accident'),
    (
        ('Other abnormallaboratory tests(other than tests listed above '
         'or tests done as part of this study), specify test and result'),
        ('Other abnormallaboratory tests(other than tests listed above or '
         'tests done as part of this study),specify test and result')
    ),
    ('New congenital abnormality not previously identified?,specify',
     'New congenital abnormality not previously identified?,specify and '
     'complete "Congenital Anomaly"form'),
    ('Other serious (grade 3 or 4)infection(not listed above),specify',
     'Other serious (grade 3 or 4)infection(not listed above),specify'),
    ('Other serious (grade 3 or 4) non-infectious(not listed above),specify',
     'Other serious (grade 3 or 4)non-infectious(not listed above),specify'),

)

DX_MATERNAL = (
    ('Pneumonia suspected, no CXR or microbiologic confirmation',
     'Pneumonia suspected, no CXR or microbiologic confirmation'),
    ('Pneumonia, CXR confirmed, no bacterial pathogen',
     'Pneumonia, CXR confirmed, no bacterial pathogen'),
    ('Pneumonia, CXR confirmed, bacterial pathogen isolated'
     ' (specify pathogen)',
     'Pneumonia, CXR confirmed, bacterial pathogen isolated'
     ' (specify pathogen)'),
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
    (
        ('Acute diarrheal illness (bloody diarrhean OR increase of'
         ' at least 7 stools per day '
         'OR life threatening for less than 14 days'),
        ('Acute diarrheal illness (bloody diarrhean OR increase of at'
         ' least 7 stools per day '
         'OR life threatening for less than 14 days')),
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

FACIAL_DEFECT = (
    ('None', 'None'),
    ('Anophthalmia/micro-opthalmia', 'Anophthalmia/micro-opthalmia'),
    ('Cataracts', 'Cataracts'),
    ('Coloboma', 'Coloboma'),
    ('OTHER eye abnormality', 'Other eye abnormality, specify'),
    ('Absence of ear', 'Absence of ear'),
    ('Absence of auditory canal', 'Absence of auditory canal'),
    ('Congenital deafness', 'Congenital deafness'),
    ('Microtia', 'Microtia'),
    ('OTHER ear anomaly', 'Other ear anomaly, specify'),
    ('Brachial cleft cyst, sinus or pit', 'Brachial cleft cyst, sinus or pit'),
    ('OTHER facial malformation', 'Other facial malformation, specify'),
)

FEM_GENITAL_ANOMALY = (
    ('None', 'None'),
    ('Ambinguous genitalia, female', 'Ambinguous genitalia, female'),
    ('Vaginal agenesis', 'Vaginal agenesis'),
    ('Absent or streak ovary', 'Absent or streak ovary'),
    ('Uterine anomaly', 'Uterine anomaly'),
    (OTHER,
     'Other ovarian, fallopian, uterine, cervical, vaginal, or '
     'vulvar abnormality'),
)

INFO_PROVIDER = (
    ('MOTHER', 'Mother'),
    ('GRANDMOTHER', 'Grandmother'),
    ('FATHER', 'Father'),
    ('GRANDFATHER', 'Grandfather'),
    ('SIBLING', 'Sibling'),
    (OTHER, 'Other'),
)

MATERNAL_VISIT_STUDY_STATUS = (
    (ON_STUDY, 'On study'),
    (OFF_STUDY,
     'Off study-no further follow-up (including death); use only '
     'for last study contact'),
)

LOWER_GASTROINTESTINAL_ABNORMALITY = (
    ('None', 'None'),
    ('Duodenal atresia, stenosis, or absence',
     'Duodenal atresia, stenosis, or absence'),
    ('Jejunal atresis, stenosis, or absence',
     'Jejunal atresis, stenosis, or absence'),
    ('Ileal atresia, stenosis, or absence',
     'Ileal atresia, stenosis, or absence'),
    ('Atresia, stenosis, or absence of large intestine, rectum, or anus',
     'Atresia, stenosis, or absence of large intestine, rectum, or anus'),
    ('Hirschsprung disease', 'Hirschsprung disease'),
    ('OTHER megacolon', 'Other megacolon'),
    ('Liver, pancreas, or gall bladder defect, specify',
     'Liver, pancreas, or gall bladder defect, specify'),
    ('Diaphramtic hernia', 'Diaphramtic hernia'),
    ('OTHER GI anomaly', 'Other GI anomaly, specify'),
)

MALE_GENITAL_ANOMALY = (
    ('None', 'None'),
    ('Hypospadias, specify degree', 'Hypospadias, specify degree'),
    ('Chordee', 'Chordee'),
    ('Ambiguous genitalia, male', 'Ambiguous genitalia, male'),
    ('Undescended testis', 'Undescended testis'),
    (OTHER, 'Other male genital abnormality, specify'),
)

BREAST_CHOICE = (
    ('right breast', 'Right breast only'),
    ('left breast', 'Left breast only'),
    ('both breasts', 'Both breasts'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

MEDICATIONS = (
    ('Acyclovir', 'Acyclovir'),
    ('Albuterol', 'Albuterol'),
    ('Albendazol', 'Albendazol'),
    ('Aminophylline', 'Aminophylline'),
    ('Amoxicillin', 'Amoxicillin'),
    ('Ampicillin', 'Ampicillin'),
    ('Antibiotic,unknown(specify 1V or oral)',
     'Antibiotic,unknown(specify 1V or oral)'),
    ('Azithromycin', 'Azithromycin'),
    ('Carbamazepine', 'Carbamazepine'),
    ('Ceftriaxone', 'Ceftriaxone'),
    ('Cotrimoxazole (trimethoprim/sulfamethoxazole)',
     'Cotrimoxazole (trimethoprim/sulfamethoxazole)'),
    ('Cefaclor,cefixime,ceftizoxime,ceftraxone',
     'Cefaclor,cefixime,ceftizoxime,ceftraxone'),
    ('Chloramphenicol', 'Chloramphenicol'),
    ('Ciprofloxacin', 'Ciprofloxacin'),
    ('Clarithromycin', 'Clarithromycin'),
    ('Cloxacillin', 'Cloxacillin'),
    ('Doxycycline', 'Doxycycline'),
    ('Dexamethasone', 'Dexamethasone'),
    ('Diazepam', 'Diazepam'),
    ('Erythromycin', 'Erythromycin'),
    ('Ethambutol', 'Ethambutol'),
    ('Ferrous sulfate', 'Ferrous sulfate'),
    ('Fuconazole', 'Fuconazole'),
    ('Foscarnate', 'Foscarnate'),
    ('Ganciclovir', 'Ganciclovir'),
    ('Gentamicin', 'Gentamicin'),
    ('Hydrocortisone', 'Hydrocortisone'),
    ('Insuline', 'Insuline'),
    ('Isoniazid', 'Isoniazid'),
    ('Ketoconazole', 'Ketoconazole'),
    ('Mebendazole', 'Mebendazole'),
    ('Metronidazole', 'Metronidazole'),
    ('Methylprednisolone', 'Methylprednisolone'),
    ('Nalidixic acid', 'Nalidixic acid'),
    ('Norfloxacin,Ofloxacin', 'Norfloxacin,Ofloxacin'),
    ('Pentamidine', 'Pentamidine'),
    ('Pyridoxine', 'Pyridoxine'),
    ('Phenytoin', 'Phenytoin'),
    ('Prednisolone', 'Prednisolone'),
    ('Pyrazinamide', 'Pyrazinamide'),
    ('Pyrimethamine', 'Pyrimethamine'),
    ('Quinidine', 'Quinidine'),
    ('Red blood cell transfusion', 'Red blood cell transfusion'),
    ('Rifampicin', 'Rifampicin'),
    ('Salbutamol', 'Salbutamol'),
    ('Streptomycin', 'Streptomycin'),
    ('Sulfadiazine', 'Sulfadiazine'),
    ('Terbinafine', 'Terbinafine'),
    ('Tetracycline', 'Tetracycline'),
    ('Theophylline', 'Theophylline'),
    ('Vancomycin', 'Vancomycin'),
    ('Vitamins(iron,B12,Folate)', 'Vitamins(iron,B12,Folate)'),
    ('Traditional medication', 'Traditional Medications'),
    (OTHER, 'Other, specify ...')
)

MOUTH_UP_GASTROINT_DISORDER = (
    ('None', 'None'),
    ('Aglossia', 'Aglossia'),
    ('Macroglossia', 'Macroglossia'),
    ('OTHER mouth, lip, or tongue',
     'Other mouth, lip, or tongue anomaly, specify'),
    ('Esophageal atresia', 'Esophageal atresia'),
    ('Tracheoesphageal fistula', 'Tracheoesphageal fistula'),
    ('Esophageal web', 'Esophageal web'),
    ('Pyloric stenosis', 'Pyloric stenosis'),
    ('OTHER esophageal or stomach',
     'Other esophageal or stomach abnormality, specify'),
)

MUSCULOSKELETAL_ABNORMALITY = (
    ('None', 'None'),
    ('Craniosynostosis', 'Craniosynostosis'),
    ('Torticollis', 'Torticollis'),
    ('Congenital scoliosis, lordosis', 'Congenital scoliosis, lordosis'),
    ('Congenital dislocation of hip', 'Congenital dislocation of hip'),
    ('Talipes equinovarus (club feet excluding metatarsus varus)',
     'Talipes equinovarus (club feet excluding metatarsus varus)'),
    ('Funnel chest or pigeon chest (pectus excavatum or carinaturn)',
     'Funnel chest or pigeon chest (pectus excavatum or carinaturn)'),
    ('Polydactyly', 'Polydactyly'),
    ('Syndactyly', 'Syndactyly'),
    ('Other hand malformation, specify', 'Other hand malformation, specify'),
    ('Webbed fingers or toes', 'Webbed fingers or toes'),
    ('Upper limb reduction defect, specify',
     'Upper limb reduction defect, specify'),
    ('Lower limb reduction defect, specify',
     'Lower limb reduction defect, specify'),
    ('Other limb defect, specify', 'Other limb defect, specify'),
    ('Other skull abnormality, specify', 'Other skull abnormality, specify'),
    ('Anthrogryposis', 'Anthrogryposis'),
    ('Vertebral or rib abnormalities, specify',
     'Vertebral or rib abnormalities, specify'),
    ('Osteogenesis imperfecta', 'Osteogenesis imperfecta'),
    ('Dwarfing syndrome, specify', 'Dwarfing syndrome, specify'),
    ('Congenital diaphramatic hernia', 'Congenital diaphramatic hernia'),
    ('Omphalocele', 'Omphalocele'),
    ('Gastroschisis', 'Gastroschisis'),
    (OTHER, 'Other muscular or skeletal abnormality or syndrome, specify'),
)

OTHER_DEFECT = (
    ('None', 'None'),
    (OTHER, 'Other defect/syndrome not already reported, specify'),
)

RANDOMIZATION_MATERNAL_ART_STATUS = (
    ('ON', 'On Haart'),
    ('OFF', 'Off'),
)

RANDOMIZATION_MATERNAL_FEEDING_CHOICE = (
    ('FF', 'Formula'),
    ('BF', 'Breast'),
)

RANDOMIZATION_SITE = (
    ('Molepolole', 'Molepolole'),
    ('Lobatse', 'Lobatse'),
    ('Gaborone', 'Gaborone'),
)

REASON_RCV_FORMULA = (
    ('no milk', '1. Mother did not have enough breast milk'),
    ('back to work',
     '2. Mother returned to work so unable to breastfeed '
     'participant exclusively'),
    ('off HAART',
     '3. Mother stopped breastfeeding because no longer taking HAART'),
    ('afraid to transmit', ('4. Mother stopped because she is '
                            'afraid she will transmit HIV '
                            'to the participant even though '
                            'she\'s taking HAART')),
    ('advised to mix feed',
     '5. Mother advised to add other food/liquids by partner/family'),
    ('felt to mix feed', ('6. Mother felt that baby needed other '
                          'foods/liquids to be healthy '
                          '(for babies <= 6 months old)')),
    ('complete per protocol', ('7. <Per breastfeeding randomisation, '
                               'infant is >5 months or >11 '
                               'months of age and completed breastfeeding '
                               'per protocol')),
    (OTHER, '9. Other'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

REASON_MISSED_CTX_PLACEBO = (
    ('caregiver forgot', 'Caregiver forgot to give the CTX/Placebo'),
    ('caregiver ran out/lost',
     'Caregiver ran out of CTX/Placebo or lost the bottle'),
    ('caregiver away',
     'Primary caregiver was away from home and did not have another '
     'person give the CTX/Placebo'),
    ('infant away',
     'Infant was away from home and the CTX/Placebo bottle was not '
     'at the other location'),
    ('caregiver decision/sick',
     'Caregiver chose not to give the CTX/Placebo because baby was '
     'ick or for other reasons'),
    (OTHER, 'Other'),
    (NOT_APPLICABLE, 'Not Applicable'),
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

REASON_MISSED_PROPHYLAXIS = (
    ('caregiver forgot', 'Caregiver forgot to give the NVP'),
    ('caregiver ran out/lost', 'Caregiver ran out of NVP or lost the bottle'),
    ('caregiver away',
     'Primary caregiver was away from home and did not have another '
     'person give the NVP'),
    ('infant away',
     'Infant was away from home and the NVP bottle was not at '
     'the other location'),
    ('caregiver decision/sick',
     'Caregiver chose not to give the NVP because baby was sick or '
     'for other reasons'),
    (OTHER, 'Other'),
)

RENAL_ANOMALY = (
    ('None', 'None'),
    ('Bilateral renal agenesis', 'Bilateral renal agenesis'),
    ('Unilateral renal agenesis or dysplasia',
     'Unilateral renal agenesis or dysplasia'),
    ('Polycystic kidneys', 'Polycystic kidneys'),
    ('Congenital hydronephrosis', 'Congenital hydronephrosis'),
    ('Unilateral stricture, stenosis, or hypoplasia',
     'Unilateral stricture, stenosis, or hypoplasia'),
    ('Duplicated kidney or collecting system',
     'Duplicated kidney or collecting system'),
    ('Horseshoe kidney', 'Horseshoe kidney'),
    ('Exstrophy of bladder', 'Exstrophy of bladder'),
    ('Posterior urethral valves', 'Posterior urethral valves'),
    (OTHER, 'Other renal, ureteral, bladder, urethral abnormality, specify'),
)

RESPIRATORY_DEFECT = (
    ('None', 'None'),
    ('Choanal atresia', 'Choanal atresia'),
    ('Agenesis or underdevelopment of nose',
     'Agenesis or underdevelopment of nose'),
    ('Nasal cleft', 'Nasal cleft'),
    ('Single nostril, proboscis', 'Single nostril, proboscis'),
    ('OTHER nasal or sinus abnormality',
     'Other nasal or sinus abnormality, specify'),
    ('Lryngeal web. glottic or subglottic',
     'Lryngeal web. glottic or subglottic'),
    ('Congenital laryngeal stenosis', 'Congenital laryngeal stenosis'),
    ('OTHER laryngeal, tracheal or bronchial anomalies',
     'Other laryngeal, tracheal or bronchial anomalies'),
    ('Single lung cyst', 'Single lung cyst'),
    ('Polycystic lung', 'Polycystic lung'),
    (OTHER, 'Other respiratory anomaly, specify'),
)

STUDY_STATUS = (
    ('followup', 'Lost can followup'),
    ('no followup', 'Lost no followup'),
)

SKIN_ABNORMALITY = (
    ('None', 'None'),
    ('Icthyosis', 'Icthyosis'),
    ('Ectodermal dysplasia', 'Ectodermal dysplasia'),
    (OTHER, 'Other skin abnormality, specify'),
)

SKIP_MEALS_FREQUEENCY = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('dont_know', 'Don\'t know')
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

TRISOME_CHROSOMESOME_ABNORMALITY = (
    ('None', 'None'),
    ('Trisomy 21', 'Trisomy 21'),
    ('Trisomy 13', 'Trisomy 13'),
    ('Trisomy 18', 'Trisomy 18'),
    ('OTHER trisomy, specify', 'Other trisomy, specify'),
    ('OTHER non-trisomic chromosome',
     'Other non-trisomic chromosome abnormality, specify'),
)

VACCINES = (
    ('HBV', 'HBV'),
    ('BCG', 'BCG'),
    ('DTap', 'DTap'),
    ('Hib', 'Hib'),
    ('Polio', 'Polio'),
    ('Pneumoccal_Vaccine', 'Pneumoccal Vaccine'),
    ('Rotavirus', 'Rotavirus'),
    ('MMR', 'MMR'),
    ('Varicella', 'Varicella'),
    ('Influenza', 'Influenza'),
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

STOOL_TEXTURE_DESC = (
    ('formed_with_blood', 'Formed without blood'),
    ('formed_without_blood', 'Formed with blood'),
    ('loose_without_blood', 'Loose but not watery and without blood'),
    ('loose_with_blood', 'Loose but not watery and with blood'),
    ('watery_without_blood', 'Watery without blood'),
    ('watery_with_blood', 'Watery with blood'),
)

ILLNESS_CLASSIFICATION = (
    (NOT_APPLICABLE, 'Not applicable'),
    ('respi_illness', 'Respiratory Illness'),
    ('gastro_illness',
     'Gastrointestinal illness (examples including vomiting, '
     'diarrhea or both)'),
    (OTHER, 'Other'),
)

STOOLS_PAST_24HOURS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('>7', '>7'),
    (UNKNOWN, 'Unknown')
)

CONTINUOUS_LOOSE_STOOLS = (
    ('1day', '1 day'),
    ('2days', '2 days'),
    ('3days', '3 days'),
    ('4days', '4 days'),
    ('5days', '5 days'),
    ('6days', '6 days'),
    ('7days', '7 days'),
    ('>7days', 'Greater than 7 days but not more than 13 days'),
    ('>14days', '14 days or greater')
)

ARV_STATUS_WITH_NEVER = (
    (NO_MODIFICATIONS,
     '1. No modifications made since the last attended scheduled'
     ' visit or today'),
    (START,
     '2. Starting today or has started since last attended scheduled visit'),
    (NEVER_STARTED, '3. Never started'),
    (MODIFIED,
     '4. Change in at least one medication since the last attended'
     ' scheduled visit or today'),
)

CIRCUMCISION = (
    ('CIRC', 'circumcised'),
    ('UNCIRC', 'uncircumcised'),
)

GESTATIONS_NUMBER = (
    ('0', '0'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3')
)

ZERO_ONE = (
    ('0', '0'),
    ('1', '1')
)

MALFORMATIONS = (
    ('choroid_plexus_cyst', 'choroid plexus cyst'),
    ('intracranial_calcification', 'intracranial calcification'),
    ('posterior_fossa_cyst', 'posterior fossa cyst'),
    ('intracranial_cyst', 'intracranial cyst'),
    ('other', 'other')
)

DIAGNOSES = (
    ('Gestational Hypertension', 'Gestational Hypertension'),
    ('Pre-eclampsia', 'Pre-eclampsia'),
    ('Liver Problems', 'Liver Problems'),
    ('Genital Herpes', 'Genital Herpes'),
    ('Syphillis', 'Syphillis'),
    ('Gonorrhea', 'Gonorrhea'),
    ('Chlamydia', 'Chlamydia'),
    ('Hepatitis B surface Ag positive', 'Hepatitis B surface Ag positive'),
    ('Hepatitis C', 'Hepatitis C'),
    ('Depression', 'Depression'),
    ('Tuberculosis', 'Tuberculosis'),
    ('Asthma requiring steroids', 'Asthma requiring steroids'),
    ('Pneumonia', 'Pneumonia'),
    ('Other', 'Other')
)

HOSPITALIZATION_REASON = (
    ('Pneumonia or other respiratory disease',
     'Pneumonia or other respiratory disease'),
    ('Postpartum infection', 'Postpartum infection (wound/laceration)'),
    ('Bowel obstruction', 'Bowel obstruction'),
    ('Endometritis', 'Endometritis'),
    ('Unexplained fever', 'Unexplained fever'),
    ('Other', 'Other')
)

LAUGH = (
    ('As much as I always could', 'As much as I always could'),
    ('Not quite so much now', 'Not quite so much now'),
    ('Definitely not so much now', 'Definitely not so much now'),
    ('Not at all', 'Not at all')
)

ENJOYMENT = (
    ('As much as I ever did', 'As much as I ever did'),
    ('Rather less than I used to', 'Rather less than I used to'),
    ('Definitely less than I used to', 'Definitely less than I used to'),
    ('Hardly at all', 'Hardly at all')
)

BLAME = (
    ('Yes, most of the time', 'Yes, most of the time'),
    ('Yes, some of the time', 'Yes, some of the time'),
    ('Not very often', 'Not very often'),
    ('No, never', 'No, never')
)

UNHAPPY = BLAME

SAD = BLAME

ANXIOUS = (
    ('No, not at all', 'No, not at all'),
    ('Hardly ever', 'Hardly ever'),
    ('Yes, sometimes', 'Yes, sometimes'),
    ('Yes, very often', 'Yes, very often')
)

PANICK = (
    ('Yes, quite a lot', 'Yes, quite a lot'),
    ('Yes, sometimes', 'Yes, sometimes'),
    ('No, not much', 'No, not much'),
    ('No, not at all', 'No, not at all')
)

TOP = (
    ('Yes, most of the time I haven\'t been able to cope at all',
     'Yes, most of the time I haven\'t been able to cope at all'),
    ('Yes, sometimes I haven\'t been coping as well as usual',
     'Yes, sometimes I haven\'t been coping as well as usual'),
    ('No, most of the time I have coped quite well',
     'No, most of the time I have coped quite well'),
    ('No, I have been coping as well as ever',
     'No, I have been coping as well as ever')
)

CRYING = (
    ('Yes, most of the time', 'Yes, most of the time'),
    ('Yes, quite often', 'Yes, quite often'),
    ('Only occasionally', 'Only occasionally'),
    ('No, never', 'No, never')
)

HARM = (
    ('Yes, quite often', 'Yes, quite often'),
    ('Sometimes', 'Sometimes'),
    ('Hardly ever', 'Hardly ever'),
    ('Never', 'Never')
)

AMNIOTIC_FLUID = (
    ('0', 'Normal'),
    ('1', 'Abnormal')
)

REASON_ARV_STOP = (
    ('switch for tolerability', 'Switch for tolerability'),
    ('switch for drug outage', 'Switch for drug outage'),
    ('Treatment failure', 'Treatment failure'),
    (OTHER, 'Other, specify:')
)

REASON_NOT_DRAWN = (
    ('collection_failed', 'Tried, but unable to obtain sample from patient'),
    ('absent', 'Patient did not attend visit'),
    ('refused', 'Patient refused'),
    ('no_supplies', 'No supplies'),
    (OTHER, 'Other'),)

CAUSE_OF_DEATH = (
    ('cryptococcal_meningitis', 'Cryptococcal meningitis'),
    ('Cryptococcal_meningitis_relapse_IRIS',
     'Cryptococcal meningitis relapse/IRIS'),
    (TUBERCULOSIS, 'TB'),
    ('bacteraemia', 'Bacteraemia'),
    ('bacterial_pneumonia', 'Bacterial pneumonia'),
    ('malignancy', 'Malignancy'),
    ('art_toxicity', 'ART toxicity'),
    ('IRIS_non_CM', 'IRIS non-CM'),
    ('diarrhea_wasting', 'Diarrhea/wasting'),
    (UNKNOWN, 'Unknown'),
    (OTHER, 'Other'),
)

SOURCE_OF_DEATH_INFO = (
    ('autopsy', 'Autopsy'),
    ('clinical_records', 'Clinical_records'),
    ('study_staff',
     'Information from study care taker staff prior participant death'),
    ('health_care_provider',
     'Contact with other (non-study) physician/nurse/other health care provider'),
    ('death_certificate', 'Death Certificate'),
    ('relatives_friends',
     'Information from participant\'s relatives or friends'),
    ('obituary', 'Obituary'),
    ('pending_information', 'Information requested, still pending'),
    ('no_info', 'No information will ever be available'),
    (OTHER, 'Other, specify'),)

CAUSE_OF_DEATH_CAT = (
    ('hiv_related', 'HIV infection or HIV related diagnosis'),
    ('hiv_unrelated', 'Disease unrelated to HIV'),
    ('study_drug', 'Toxicity from Study Drug'),
    ('non_study_drug', 'Toxicity from non-Study drug'),
    ('trauma', 'Trauma/Accident'),
    ('no_info', 'No information available'),
    (OTHER, 'Other, specify'),)

MED_RESPONSIBILITY = (
    ('doctor', 'Doctor'),
    ('nurse', 'Nurse'),
    ('traditional', 'Traditional Healer'),
    ('all', 'Both Doctor or Nurse and Traditional Healer'),
    ('none', 'No known medical care received (family/friends only)'),)

HOSPITILIZATION_REASONS = (
    ('respiratory illness(unspecified)', 'Respiratory Illness(unspecified)'),
    ('respiratory illness, cxr confirmed',
     'Respiratory Illness, CXR confirmed'),
    ('respiratory illness, cxr confirmed, bacterial pathogen, specify',
     'Respiratory Illness, CXR confirmed, bacterial pathogen, specify'),
    ('respiratory illness, cxr confirmed, tb or probable tb',
     'Respiratory Illness, CXR confirmed, TB or probable TB'),
    ('diarrhea illness(unspecified)', 'Diarrhea Illness(unspecified)'),
    ('diarrhea illness, viral or bacterial pathogen, specify',
     'Diarrhea Illness, viral or bacterial pathogen, specify'),
    ('sepsis(unspecified)', 'Sepsis(unspecified)'),
    ('sepsis, pathogen specified, specify',
     'Sepsis, pathogen specified, specify'),
    ('mengitis(unspecified)', 'Mengitis(unspecified)'),
    ('mengitis, pathogen specified, specify',
     'Mengitis, pathogen specified, specify'),
    ('non-infectious reason for hospitalization, specify',
     'Non-infectious reason for hospitalization, specify'),
    (OTHER, 'Other infection, specify'),
)

TB_SITE_DEATH = (
    ('meningitis', 'Meningitis'),
    ('pulmonary', 'Pulmonary'),
    ('disseminated', 'Disseminated'),
    (NOT_APPLICABLE, 'Not applicable')
)

FAMILY_RELATION = (

    ('me', 'Me'),
    ('father', 'Father'),
    ('sibling', 'Sibling'),
    ('grandmother', 'Grandmother'),
    ('grandfather', 'Grandfather'),
    ('aunt', 'Aunt'),
    ('uncle', 'Uncle'),
    (NOT_APPLICABLE, 'Not applicable'),
)

POS_NEG_PENDING = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    ('pending', 'Pending')
)

REASON_NOT_DRAWN = (
    (NOT_APPLICABLE, 'Not applicable'),
    ('collection_failed', 'Tried, but unable to obtain sample from patient'),
    ('absent', 'Patient did not attend visit'),
    ('refused', 'Patient refused'),
    ('no_supplies', 'No supplies'),
    ('other', 'Other'),
)

YES_NO_TRIED = (
    (YES, YES),
    (NO, NO),
    ('tried', 'Tried, but could not get tested'),
    (UNKNOWN, 'Unknown'),
)
