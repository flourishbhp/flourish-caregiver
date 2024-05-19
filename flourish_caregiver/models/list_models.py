from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_mixins import ListModelMixin as BaseListModelMixin


class ListModelMixin(BaseListModelMixin):
    name = models.CharField(
        verbose_name='Name',
        max_length=250,
        db_index=True,
        help_text='(suggest 40 characters max.)',
    )

    class Meta:
        abstract = True


class ChronicConditions(ListModelMixin, BaseUuidModel):
    pass


class CaregiverMedications(ListModelMixin, BaseUuidModel):
    pass


class DeliveryComplications(ListModelMixin, BaseUuidModel):
    pass


class EmoSupportType(ListModelMixin, BaseUuidModel):
    pass


class EmoHealthImproved(ListModelMixin, BaseUuidModel):
    pass


class MaternalDiagnosesList(ListModelMixin, BaseUuidModel):
    pass


class PriorArv(ListModelMixin, BaseUuidModel):
    pass


class PhoneNumType(ListModelMixin, BaseUuidModel):
    pass


class WcsDxAdult(ListModelMixin, BaseUuidModel):
    pass


class CovidSymptoms(ListModelMixin, BaseUuidModel):
    pass


class CovidSymptomsAfter14Days(ListModelMixin, BaseUuidModel):
    pass


class CaregiverSocialWorkReferralList(ListModelMixin, BaseUuidModel):
    pass


class PregnancyInfluencersList(ListModelMixin, BaseUuidModel):
    pass


class AfterPregnancyInfluencersList(ListModelMixin, BaseUuidModel):
    pass


class ReceivedTrainingOnFeedingList(ListModelMixin, BaseUuidModel):
    pass


class ReasonsForInfantFeedingList(ListModelMixin, BaseUuidModel):
    pass


class TbKnowledgeMedium(ListModelMixin, BaseUuidModel):
    pass


class TbDiagnostics(ListModelMixin, BaseUuidModel):
    pass


class TbVisitCareLocation(ListModelMixin, BaseUuidModel):
    pass


class HouseholdMember(ListModelMixin, BaseUuidModel):
    pass


class MemberReadBooks(ListModelMixin, BaseUuidModel):
    pass


class MemberToldStories(ListModelMixin, BaseUuidModel):
    pass


class MemberSangSongs(ListModelMixin, BaseUuidModel):
    pass


class MemberChildOutside(ListModelMixin, BaseUuidModel):
    pass


class MemberPlayedWithChild(ListModelMixin, BaseUuidModel):
    pass


class MemberNamedWithChild(ListModelMixin, BaseUuidModel):
    pass


class ArvInterruptionReasons(ListModelMixin, BaseUuidModel):
    pass


class ExpenseContributors(ListModelMixin, BaseUuidModel):
    pass


class TBTests(ListModelMixin, BaseUuidModel):
    pass


class GeneralSymptoms(ListModelMixin, BaseUuidModel):
    pass


class MastitisActions(ListModelMixin, BaseUuidModel):
    pass


class CrackedNipplesActions(ListModelMixin, BaseUuidModel):
    pass
