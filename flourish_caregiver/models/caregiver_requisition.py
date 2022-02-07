from django.apps import apps as django_apps
from django.conf import settings
from django.db import models
from django.db.models.deletion import PROTECT
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_constants.constants import NOT_APPLICABLE
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_lab.choices import PRIORITY
from edc_lab.models import RequisitionIdentifierMixin
from edc_lab.models import RequisitionModelMixin, RequisitionStatusMixin
from edc_metadata.model_mixins.updates import UpdatesRequisitionMetadataModelMixin
from edc_reference.model_mixins import RequisitionReferenceModelMixin
from edc_search.model_mixins import SearchSlugManager

from edc_visit_schedule.model_mixins import SubjectScheduleCrfModelMixin
from edc_visit_tracking.managers import CrfModelManager as VisitTrackingCrfModelManager
from edc_visit_tracking.model_mixins import CrfModelMixin as VisitTrackingCrfModelMixin
from edc_visit_tracking.model_mixins import PreviousVisitModelMixin

from ..choices import STUDY_SITES, REASON_NOT_DRAWN
from .maternal_visit import MaternalVisit
from .model_mixins import SearchSlugModelMixin, ConsentVersionModelModelMixin


class Manager(VisitTrackingCrfModelManager, SearchSlugManager):
    pass


class CaregiverRequisition(
        NonUniqueSubjectIdentifierFieldMixin, ConsentVersionModelModelMixin,
        RequisitionModelMixin, RequisitionStatusMixin, RequisitionIdentifierMixin,
        VisitTrackingCrfModelMixin, SubjectScheduleCrfModelMixin,
        RequiresConsentFieldsModelMixin, PreviousVisitModelMixin,
        RequisitionReferenceModelMixin, UpdatesRequisitionMetadataModelMixin,
        SearchSlugModelMixin, BaseUuidModel):

    lab_profile_name = 'td_maternal'

    maternal_visit = models.ForeignKey(MaternalVisit, on_delete=PROTECT)

    study_site = models.CharField(
        verbose_name='Study site',
        max_length=25,
        choices=STUDY_SITES,
        default=settings.DEFAULT_STUDY_SITE)

    estimated_volume = models.DecimalField(
        verbose_name='Estimated volume in mL',
        max_digits=7,
        decimal_places=2,
        help_text=(
            'If applicable, estimated volume of sample for this test/order. '
            'This is the total volume if number of "tubes" above is greater than 1'))

    item_count = models.IntegerField(
        verbose_name='Total number of items',
        help_text=(
            'Number of tubes, samples, cards, etc being sent for this test/order only. '
            'Determines number of labels to print'))

    priority = models.CharField(
        verbose_name='Priority',
        max_length=25,
        choices=PRIORITY,
        default='normal',)

    reason_not_drawn = models.CharField(
        verbose_name='If not drawn, please explain',
        max_length=25,
        default=NOT_APPLICABLE,
        choices=REASON_NOT_DRAWN)

    comments = models.TextField(
        max_length=350,
        null=True,
        blank=True)

#     on_site = CurrentSiteManager()

    objects = Manager()

    history = HistoricalRecords()

    def __str__(self):
        return (
            f'{self.requisition_identifier} '
            f'{self.panel_object.verbose_name}')

    def save(self, *args, **kwargs):
        if not self.id:
            edc_protocol_app_config = django_apps.get_app_config(
                'edc_protocol')
            self.protocol_number = edc_protocol_app_config.protocol_number
        self.report_datetime = self.requisition_datetime
        self.subject_identifier = self.maternal_visit.subject_identifier
        super().save(*args, **kwargs)

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.extend([
            'requisition_identifier',
            'human_readable_identifier', 'identifier_prefix'])
        return fields

    class Meta:
        unique_together = ('panel', 'maternal_visit')
