from dateutil.relativedelta import relativedelta
from edc_base.utils import get_utcnow
from faker import Faker
from model_mommy.recipe import Recipe, seq

from .models import Enrollment, SubjectConsent


fake = Faker()

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

enrollment = Recipe(
    Enrollment,
)
