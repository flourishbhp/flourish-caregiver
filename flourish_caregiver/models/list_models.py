from edc_base.model_mixins import BaseUuidModel, ListModelMixin


class ChronicConditions(ListModelMixin, BaseUuidModel):
    pass


class CaregiverMedications(ListModelMixin, BaseUuidModel):
    pass


class DeliveryComplications(ListModelMixin, BaseUuidModel):
    pass


class EmoSupportType(ListModelMixin, BaseUuidModel):
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
