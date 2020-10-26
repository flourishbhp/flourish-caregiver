from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_validators import datetime_not_future
from edc_base.utils import get_utcnow
from ..choices import REFERRED_TO
from .model_mixins import CrfModelMixin


class ReferredTo(CrfModelMixin):

    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, ], )

    referred_to = models.CharField(
        verbose_name='Referred To',
        choices=REFERRED_TO,
        max_length=50)

    referred_to_other = OtherCharField()

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_maternal'
        verbose_name = 'Referred To'
        verbose_name_plural = 'Referred To'
