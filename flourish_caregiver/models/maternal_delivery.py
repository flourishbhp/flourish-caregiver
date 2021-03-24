from django.apps import apps as django_apps
from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.model_validators.date import date_not_future
from edc_constants.choices import YES_NO, YES_NO_NA
from edc_constants.constants import YES, POS
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin
from edc_protocol.validators import datetime_not_before_study_start

from ..maternal_choices import (
    DELIVERY_HEALTH_FACILITY, DELIVERY_MODE, CSECTION_REASON)
from ..choices import FEEDING_CHOICES
from .list_models import DeliveryComplications


class MaternalDelivery(UniqueSubjectIdentifierFieldMixin, BaseUuidModel):

    """ A model completed by the user on Maternal Delivery which
    triggers registration of infants.
    """

    report_datetime = models.DateTimeField(
        verbose_name="Report date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        help_text='')

    delivery_datetime = models.DateTimeField(
        verbose_name="Date and time of delivery :",
        help_text="If TIME unknown, estimate",
        validators=[
            datetime_not_future, ])

    delivery_time_estimated = models.CharField(
        verbose_name="Is the delivery TIME estimated?",
        max_length=3,
        choices=YES_NO)

    delivery_hospital = models.CharField(
        verbose_name="Place of delivery? ",
        max_length=65,
        choices=DELIVERY_HEALTH_FACILITY,
        help_text="If 'OTHER', specify below")

    delivery_hospital_other = OtherCharField()

    labour_hrs = models.CharField(
        verbose_name="How long prior to delivery, in HRS, did labour begin? ",
        max_length=10)

    mode_delivery = models.CharField(
        verbose_name="What was the mode of delivery?",
        max_length=100,
        choices=DELIVERY_MODE,
        help_text="If 'OTHER', specify below")

    mode_delivery_other = OtherCharField()

    csection_reason = models.CharField(
        verbose_name="If C-section was performed, indicate reason below",
        max_length=100,
        choices=CSECTION_REASON,
        help_text="If 'OTHER', specify below")

    csection_reason_other = OtherCharField()

    delivery_complications = models.ManyToManyField(
        DeliveryComplications,
        verbose_name="Were any of the following complications present "
        "at delivery? ",
        blank=False,
        help_text="If 'OTHER', specify below")

    delivery_complications_other = OtherCharField()

    live_infants_to_register = models.IntegerField(
        verbose_name="How many babies are you registering to the study? ")

    still_births = models.IntegerField(
        default=0,
        verbose_name="How many still births or miscarriages?")

    valid_regiment_duration = models.CharField(
        verbose_name="(Interviewer) If HIV+ve, has the participant been "
        "on the ART regimen for at least 4 weeks in pregnancy?",
        choices=YES_NO_NA,
        null=True,
        blank=False,
        max_length=15,
        help_text=("If not 4 or more weeks then participant will go "
                   "OFF STUDY."))

    arv_initiation_date = models.DateField(
        verbose_name="(Interviewer) If on ART, when did the participant "
        "initiate therapy for this pregnancy?",
        validators=[date_not_future],
        null=True,
        blank=True)

    delivery_comment = models.TextField(
        verbose_name="List any additional information about the labour "
        "and delivery (mother only) ",
        max_length=250,
        blank=True,
        null=True)

    comment = models.TextField(
        verbose_name="Comment if any additional pertinent information ",
        max_length=250,
        blank=True,
        null=True)

    feeding_mode = models.CharField(
        verbose_name='How was the infant being fed immediately after delivery?',
        choices=FEEDING_CHOICES,
        max_length=100)

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.subject_identifier}'

    @property
    def antenatal_enrollment(self):
        AntenatalEnrollment = django_apps.get_model(
            'flourish_caregiver.antenatalenrollment')
        return AntenatalEnrollment.objects.get(
            subject_identifier=self.subject_identifier)

    @property
    def keep_on_study(self):
        if (self.antenatal_enrollment.enrollment_hiv_status == POS
                and self.valid_regiment_duration != YES):
            return False
        return True

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = "Birth Form"
        verbose_name_plural = "Birth Form"
