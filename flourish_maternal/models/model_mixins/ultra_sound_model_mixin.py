from django.apps import apps as django_apps
from django.db import models

from ...choices import AMNIOTIC_FLUID
from ...validators import validate_bpd, validate_hc, validate_ac, validate_fl


class UltraSoundModelMixin(models.Model):

    """ The base ultra sound model. """

    bpd = models.DecimalField(
        verbose_name="BPD?",
        validators=[validate_bpd, ],
        max_digits=6,
        decimal_places=2,
        help_text='Units in cm.')

    hc = models.DecimalField(
        verbose_name="HC?",
        validators=[validate_hc, ],
        max_digits=6,
        decimal_places=2,
        help_text='Units in cm.')

    ac = models.DecimalField(
        verbose_name="AC?",
        validators=[validate_ac, ],
        max_digits=6,
        decimal_places=2,
        help_text='Units in cm.')

    fl = models.DecimalField(
        verbose_name="FL?",
        validators=[validate_fl, ],
        max_digits=6,
        decimal_places=2,
        help_text='Units in cm.')

    amniotic_fluid_volume = models.CharField(
        verbose_name="Amniotic fluid volume?",
        max_length=10,
        choices=AMNIOTIC_FLUID,
        help_text='')

    @property
    def antenatal_enrollment(self):
        AntenatalEnrollment = django_apps.get_model(
            'td_maternal.antenatalenrollment')
        return AntenatalEnrollment.objects.get(
            subject_identifier=self.maternal_visit.subject_identifier)

    class Meta:
        abstract = True
