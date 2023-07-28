from django.apps import apps as django_apps
from django.db import models
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django_crypto_fields.fields import EncryptedCharField
from django_crypto_fields.fields import FirstnameField, LastnameField
from edc_action_item.model_mixins import ActionModelMixin
from edc_action_item.action import ActionItemGetter
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import CellNumber, TelephoneNumber
from edc_base.model_validators.date import date_not_future, datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO, YES_NO_DOESNT_WORK, YES_NO_NA
from edc_locator.model_mixins.subject_contact_fields_mixin import SubjectContactFieldsMixin
from edc_locator.model_mixins.subject_indirect_contact_fields_mixin import SubjectIndirectContactFieldsMixin
from edc_locator.model_mixins.subject_work_fields_mixin import SubjectWorkFieldsMixin
from edc_locator.model_mixins.locator_methods_model_mixin import LocatorMethodsModelMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_search.model_mixins import SearchSlugManager

from ..identifiers import ScreeningIdentifier
from ..action_items import CAREGIVER_LOCATOR_ACTION
from .model_mixins import SearchSlugModelMixin
from .dataset_action_item import DataSetActionItem


class LocatorManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, subject_identifier):
        return self.get(subject_identifier=subject_identifier)


class CaregiverLocator(SiteModelMixin, SubjectContactFieldsMixin,
                       SubjectIndirectContactFieldsMixin, ActionModelMixin,
                       SubjectWorkFieldsMixin, LocatorMethodsModelMixin,
                       SearchSlugModelMixin, BaseUuidModel):

    identifier_cls = ScreeningIdentifier

    action_name = CAREGIVER_LOCATOR_ACTION

    tracking_identifier_prefix = 'SL'

    report_datetime = models.DateTimeField(
        default=get_utcnow,
        validators=[datetime_not_before_study_start, datetime_not_future])

    screening_identifier = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        blank=True,
        null=True,
        unique=True)

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        blank=True,
        null=True, )

    study_maternal_identifier = models.CharField(
        verbose_name="Study Caregiver Subject Identifier",
        max_length=50,
        blank=True,
        null=True)

    first_name = FirstnameField(
        verbose_name='First name',
        null=True, blank=False)

    last_name = LastnameField(
        verbose_name='Last name',
        null=True, blank=False)

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
        choices=YES_NO_NA,
        verbose_name=mark_safe(
            'Has the participant given his/her permission for study '
            'staff to call her for follow-up purposes during the study?'))

    may_visit_home = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name=mark_safe(
            'Has the participant given his/her permission for study staff <b>to '
            'make home visits</b> for follow-up purposes during the study?'))

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

    is_locator_updated = models.CharField(
        verbose_name='Did you make any changes to this form',
        choices=YES_NO,
        null=True,
        blank=True,
        max_length=5
    )
   

    history = HistoricalRecords()

    objects = LocatorManager()

    @property
    def action_item(self):
        """Returns the ActionItem instance associated with
        this model or None.
        """
        action_item_cls = django_apps.get_model('edc_action_item.actionitem')

        if (not self.subject_identifier
                or self.subject_identifier == self.study_maternal_identifier):
            action_item_cls = DataSetActionItem
        try:
            action_item = action_item_cls.objects.get(
                action_identifier=self.action_identifier)
        except action_item_cls.DoesNotExist:
            action_item = None
        return action_item

    def save(self, *args, **kwargs):
        if not self.subject_identifier and not self.action_identifier:
            action_item_cls = ActionItemGetter.action_item_model_cls()
            action_item_obj = action_item_cls.objects.create(
                action_type=self.action_cls.action_type())
            self.action_identifier = action_item_obj.action_identifier
        # if self.subject_identifier is not None:
        #    self.update_action_item()

        super().save(*args, **kwargs)

    def update_action_item(self):
        """Updates the ActionItem instance associated with
        this model or None.
        """
        action_item_cls = django_apps.get_model('edc_action_item.actionitem')
        try:
            action_item_obj = action_item_cls.objects.get(
                action_identifier=self.action_identifier)
        except action_item_cls.DoesNotExist:
            raise ValidationError('Missing associated ActionItem instance')
        else:
            if not action_item_obj.subject_identifier:
                action_item_obj.subject_identifier = self.subject_identifier
                action_item_obj.save()

    def update_locator_subject_identifier(self):
        locator_cls = django_apps.get_model('flourish_caregiver.caregiverlocator')
        try:
            locator_obj = locator_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except locator_cls.DoesNotExist:
            pass
        else:
            locator_obj.subject_identifier = self.subject_identifier
            locator_obj.save()

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Locator'
