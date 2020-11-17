from edc_base.model_mixins import BaseUuidModel, ListModelMixin


class ChronicConditions(ListModelMixin, BaseUuidModel):
    pass


class CaregiverMedications(ListModelMixin, BaseUuidModel):
    pass


class DeliveryComplications(ListModelMixin, BaseUuidModel):
    pass


class MaternalDiagnosesList(ListModelMixin, BaseUuidModel):
    pass


class PriorArv (ListModelMixin, BaseUuidModel):
    pass


class WcsDxAdult(ListModelMixin, BaseUuidModel):
    pass
