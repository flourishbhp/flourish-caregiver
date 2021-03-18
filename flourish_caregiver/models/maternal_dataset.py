from django.db import models
from django_crypto_fields.fields import FirstnameField, LastnameField
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin

from ..identifiers import ScreeningIdentifier
from .model_mixins import SearchSlugModelMixin


class MaternalDataset(NonUniqueSubjectIdentifierFieldMixin,
                      SiteModelMixin, SearchSlugModelMixin,
                      BaseUuidModel):

    identifier_cls = ScreeningIdentifier

    screening_identifier = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        blank=True,
        null=True,
        unique=True)

    study_maternal_identifier = models.CharField(
        verbose_name="Study maternal Subject Identifier",
        max_length=50,
        unique=True)

    first_name = FirstnameField(null=True, blank=False)

    last_name = LastnameField(null=True, blank=False)

    protocol = models.CharField(max_length=150)

    delivdt = models.DateField(
        verbose_name='Delivery date')

    site_name = models.CharField(max_length=150)

    mom_enrolldate = models.DateField(
        verbose_name='Maternal enrollment date')

    delivmeth = models.CharField(
        verbose_name='Method of delivery',
        max_length=150, blank=True, null=True)

    delivery_location = models.CharField(
        verbose_name='Delivery location',
        max_length=150, blank=True, null=True)

    ega_delivery = models.IntegerField(
        verbose_name='EGA at delivery',
        blank=True, null=True)

    mom_age_enrollment = models.CharField(
        verbose_name='Mother\'s age at enrollment',
        max_length=150,
        blank=True, null=True)

    mom_hivstatus = models.CharField(
        verbose_name='Maternal HIV infection status',
        max_length=150)

    parity = models.IntegerField(blank=True, null=True)

    gravida = models.IntegerField(blank=True, null=True)

    mom_education = models.CharField(
        verbose_name='Maternal education level',
        max_length=150)

    mom_maritalstatus = models.CharField(
        verbose_name='Maternal marital status',
        max_length=150)

    mom_personal_earnings = models.CharField(
        verbose_name='Mother\'s personal earnings',
        max_length=150,
        blank=True, null=True)

    mom_moneysource = models.CharField(
        verbose_name='Maternal source of income',
        max_length=150)

    mom_occupation = models.CharField(
        verbose_name='Mother\'s occupation',
        max_length=150)

    mom_pregarv_strat = models.CharField(
        verbose_name='Maternal ARVs during pregnancy',
        max_length=150, blank=True, null=True)

    mom_arvstart_date = models.DateField(
        verbose_name='Date mother started HAART',
        blank=True, null=True)

    mom_baseline_cd4 = models.IntegerField(
        verbose_name='Maternal baseline CD4 count',
        blank=True, null=True)

    mom_baseline_cd4date = models.DateField(
        verbose_name='Draw data of mother\'s baseline CD4',
        blank=True, null=True)

    mom_baseline_vl = models.IntegerField(
        verbose_name='Maternal baseline viral load',
        blank=True, null=True)

    mom_baseline_vldate = models.DateField(
        verbose_name='Draw date of mother\'s baseline VL',
        blank=True, null=True)

    mom_baseline_hgb = models.DecimalField(
        verbose_name='Maternal baseline HGB',
        decimal_places=1, max_digits=10,
        blank=True, null=True)

    mom_baseline_hgbdt = models.DateField(
        verbose_name='Date of maternal baseline HGB',
        blank=True, null=True)

    mom_deathdate = models.DateField(
        verbose_name='Date mother died',
        blank=True, null=True)

    cooking_method = models.CharField(
        verbose_name='Primary cooking method',
        max_length=200, blank=True, null=True)

    home_eletrified = models.CharField(
        verbose_name='Electricity in home',
        max_length=150, blank=True, null=True)

    house_type = models.CharField(
        verbose_name='Type of dwelling',
        max_length=150, blank=True, null=True)

    toilet = models.CharField(
        verbose_name='Toilet facilities',
        max_length=150,
        blank=True, null=True)

    toilet_indoors = models.CharField(
        verbose_name='House has indoor toilet',
        max_length=150, blank=True, null=True)

    toilet_private = models.CharField(
        verbose_name='Private toilet for compound',
        max_length=150, blank=True, null=True)

    piped_water = models.CharField(
        verbose_name='Water piped into home',
        max_length=150, blank=True, null=True)

    home_refridgeration = models.CharField(
        verbose_name='Refrigeration in home',
        max_length=150, blank=True, null=True)

    drinking_water = models.CharField(
        verbose_name='Source of drinking water',
        max_length=150, blank=True, null=True)

    live_inhouse_number = models.IntegerField(
        verbose_name='Number of people living in household',
        blank=True, null=True)

    twin_triplet = models.IntegerField(
        verbose_name='Twins or thiplets',
        blank=True, null=True)

    preg_dtg = models.IntegerField(
        verbose_name='Preg DTG',
        blank=True, null=True)

    preg_pi = models.IntegerField(
        verbose_name='Preg PI',
        blank=True, null=True)

    preg_efv = models.IntegerField(
        verbose_name='Preg EFV',
        blank=True, null=True)

    on_worklist = models.BooleanField(
        default=False, blank=True, null=True)

    def __str__(self):
        return self.study_maternal_identifier

    def save(self, *args, **kwargs):
        if not self.screening_identifier:
            self.screening_identifier = self.identifier_cls().identifier
        super().save(*args, **kwargs)

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('screening_identifier')
        fields.append('study_child_identifier')
        fields.append('study_maternal_identifier')
        return fields

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Maternal Dataset'
