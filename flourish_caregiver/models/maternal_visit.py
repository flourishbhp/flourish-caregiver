from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_base.sites import CurrentSiteManager as BaseCurrentSiteManager
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_constants.choices import YES_NO_NA
from edc_consent.model_mixins import RequiresConsentFieldsModelMixin
from edc_constants.constants import ALIVE, PARTICIPANT, NOT_APPLICABLE
from edc_metadata.model_mixins.creates import CreatesMetadataModelMixin
from edc_protocol.validators import date_not_before_study_start
from edc_reference.model_mixins import ReferenceModelMixin

from edc_appointment.models import Appointment
from edc_visit_tracking.constants import MISSED_VISIT
from edc_visit_tracking.managers import VisitModelManager as BaseVisitModelManager
from edc_visit_tracking.model_mixins import VisitModelMixin, CaretakerFieldsMixin

from ..choices import MATERNAL_VISIT_STUDY_STATUS, VISIT_REASON
from ..choices import VISIT_INFO_SOURCE, ALIVE_DEAD_UNKNOWN, UNSCHEDULED_REASON
from ..helper_classes.utils import get_child_subject_identifier_by_visit
from ..visit_sequence import VisitSequence


class CurrentSiteManager(BaseVisitModelManager, BaseCurrentSiteManager):
    pass


class VisitModelManager(BaseVisitModelManager):
    use_in_migrations = True


class MaternalVisit(VisitModelMixin, CreatesMetadataModelMixin,
                    ReferenceModelMixin, RequiresConsentFieldsModelMixin,
                    CaretakerFieldsMixin, SiteModelMixin, BaseUuidModel):
    """ Maternal visit form that links all antenatal/ postnatal follow-up forms
    """

    visit_sequence_cls = VisitSequence
    appointment = models.OneToOneField(Appointment, on_delete=models.PROTECT)

    reason = models.CharField(
        verbose_name='Reason for visit',
        max_length=25,
        choices=VISIT_REASON)

    reason_missed = models.CharField(
        verbose_name='If \'missed\' above, reason scheduled visit was missed',
        blank=True,
        null=True,
        max_length=250)

    reason_unscheduled = models.CharField(
        verbose_name='If \'Unscheduled\' above, provide reason for the unscheduled visit',
        choices=UNSCHEDULED_REASON,
        blank=True,
        null=True,
        max_length=50,)

    reason_unscheduled_other = models.CharField(
        verbose_name="if unscheduled reason is Other, please specify",
        max_length=100,
        blank=True,
        null=True)

    study_status = models.CharField(
        verbose_name='What is the participant\'s current study status',
        max_length=50,
        choices=MATERNAL_VISIT_STUDY_STATUS)

    survival_status = models.CharField(
        max_length=10,
        verbose_name='Participant\'s survival status',
        choices=ALIVE_DEAD_UNKNOWN,
        null=True,
        default=ALIVE)

    info_source = models.CharField(
        verbose_name='Source of information?',
        default=PARTICIPANT,
        max_length=25,
        choices=VISIT_INFO_SOURCE)

    last_alive_date = models.DateField(
        verbose_name='Date participant last known alive',
        blank=True,
        null=True,
        validators=[date_not_before_study_start, date_not_future])

    brain_scan = models.CharField(
        verbose_name='Is participant interested infant ultrasound brain scan?',
        max_length=3,
        choices=YES_NO_NA,
        default=NOT_APPLICABLE
    )

    comments = models.TextField(
        verbose_name=(
            'Comment if any additional pertinent information '
            'about the participant'),
        blank=True,
        null=True)

    on_site = CurrentSiteManager()

    objects = VisitModelManager()

    history = HistoricalRecords()

    @property
    def child_subject_identifier(self):
        return get_child_subject_identifier_by_visit(self)

    @property
    def action_item_reason(self):
        return self.study_status

    def run_metadata_rules(self, visit=None):
        """Runs all the rule groups.

        Initially called by post_save signal.

        Also called by post_save signal after metadata is updated.
        """
        visit = visit or self

        if visit.reason not in [MISSED_VISIT, 'edc_system_glitch']:
            metadata_rule_evaluator = self.metadata_rule_evaluator_cls(
                visit=visit)
            metadata_rule_evaluator.evaluate_rules()

    class Meta(VisitModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Maternal Visit'
