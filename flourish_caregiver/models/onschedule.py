from django.apps import apps as django_apps
from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import CurrentSiteManager
from edc_identifier.managers import SubjectIdentifierManager
from edc_visit_schedule.model_mixins import OnScheduleModelMixin as BaseOnScheduleModelMixin


class OnScheduleModelMixin(BaseOnScheduleModelMixin, BaseUuidModel):
    """A model used by the system. Auto-completed by enrollment model.
    """

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50)

    child_subject_identifier = models.CharField(
        verbose_name="Associated Child Identifier",
        max_length=50)

    schedule_name = models.CharField(max_length=25, blank=True, null=True)

    on_site = CurrentSiteManager()

    objects = SubjectIdentifierManager()

    history = HistoricalRecords()

    @property
    def flourish_consent_version(self):
        consent_version_cls = django_apps.get_model('flourish_caregiver.flourishconsentversion')

        version = None
        try:
            consent_version_obj = consent_version_cls.objects.get(
                screening_identifier=self.screening_obj.screening_identifier)
        except consent_version_cls.DoesNotExist:
            version = '1'
        else:
            version = consent_version_obj.version
        return version

    @property
    def screening_obj(self):

        caregiver_consent_cls = django_apps.get_model('flourish_caregiver.subjectconsent')
        try:
            screening_obj = caregiver_consent_cls.objects.get(
                 subject_identifier=self.subject_identifier,)
        except self.caregiver_consent_cls.DoesNotExist:
            pass
        else:
            return screening_obj

    def put_on_schedule(self):
        pass

    def save(self, *args, **kwargs):
        self.consent_version = self.flourish_consent_version
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('subject_identifier', 'schedule_name')
        abstract = True


class OnScheduleCohortAEnrollment(OnScheduleModelMixin):
    pass


class OnScheduleCohortAFU(OnScheduleModelMixin):
    pass


class OnScheduleCohortAAntenatal(OnScheduleModelMixin):
    pass


class OnScheduleCohortABirth(OnScheduleModelMixin):
    pass


class OnScheduleCohortAQuarterly(OnScheduleModelMixin):
    pass


class OnScheduleCohortBEnrollment(OnScheduleModelMixin):
    pass


class OnScheduleCohortBFU(OnScheduleModelMixin):
    pass


class OnScheduleCohortBQuarterly(OnScheduleModelMixin):
    pass


class OnScheduleCohortCEnrollment(OnScheduleModelMixin):
    pass


class OnScheduleCohortCFU(OnScheduleModelMixin):
    pass


class OnScheduleCohortCQuarterly(OnScheduleModelMixin):
    pass


class OnScheduleCohortCPool(OnScheduleModelMixin):
    pass


class OnScheduleCohortASec(OnScheduleModelMixin):
    pass


class OnScheduleCohortASecQuart(OnScheduleModelMixin):
    pass


class OnScheduleCohortBSec(OnScheduleModelMixin):
    pass


class OnScheduleCohortBSecQuart(OnScheduleModelMixin):
    pass


class OnScheduleCohortCSec(OnScheduleModelMixin):
    pass


class OnScheduleCohortCSecQuart(OnScheduleModelMixin):
    pass
