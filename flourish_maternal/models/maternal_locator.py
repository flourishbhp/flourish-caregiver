from td_maternal.action_items import MATERNAL_LOCATOR_ACTION
from django.db import models
from django.utils.safestring import mark_safe
from django_crypto_fields.fields import EncryptedCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import CellNumber, TelephoneNumber
from edc_base.model_validators.date import date_not_future
from edc_base.sites import SiteModelMixin, CurrentSiteManager
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_constants.choices import YES_NO, YES_NO_DOESNT_WORK
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_action_item.model_mixins import ActionModelMixin
from edc_locator.model_mixins import LocatorModelMixin


class MaternalLocator(LocatorModelMixin, ActionModelMixin,
                      RequiresConsentFieldsModelMixin, SiteModelMixin,
                      NonUniqueSubjectIdentifierModelMixin, BaseUuidModel):

    action_name = MATERNAL_LOCATOR_ACTION

    tracking_identifier_prefix = 'SL'

    on_site = CurrentSiteManager()

    locator_date = models.DateField(
        verbose_name='Date Locator Form signed',
        validators=[date_not_future])

    health_care_infant = models.CharField(
        verbose_name=('Health clinic where your infant will'
                      ' receive their routine care'),
        max_length=35,
        blank=True,
        null=True)

    may_call = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name=mark_safe(
            'Has the participant given his/her permission for study '
            'staff to call her for follow-up purposes during the study?'))

    may_visit_home = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name=mark_safe(
            'Has the participant given his/her permission for study staff <b>to '
            'make home visits</b> for follow-up purposes during the study??'))

    has_caretaker = models.CharField(
        verbose_name=(
            "Has the participant identified someone who will be "
            "responsible for the care of the baby in case of her death, to "
            "whom the study team could share information about her baby's "
            "health?"),
        max_length=25,
        choices=YES_NO,
        help_text="")

    caretaker_name = EncryptedCharField(
        verbose_name="Full Name of the responsible person",
        max_length=35,
        help_text="include firstname and surname",
        blank=True,
        null=True)

    may_call_work = models.CharField(
        max_length=25,
        choices=YES_NO_DOESNT_WORK,
        verbose_name=mark_safe(
            'Has the participant given his/her permission for study staff '
            'to contact her at work for follow up purposes during the study?'))

    subject_work_phone = EncryptedCharField(
        verbose_name='Work contact number',
        blank=True,
        null=True)

    caretaker_cell = EncryptedCharField(
        verbose_name="Cell number",
        max_length=8,
        validators=[CellNumber, ],
        blank=True,
        null=True)

    caretaker_tel = EncryptedCharField(
        verbose_name="Telephone number",
        max_length=8,
        validators=[TelephoneNumber, ],
        blank=True,
        null=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Maternal Locator'
