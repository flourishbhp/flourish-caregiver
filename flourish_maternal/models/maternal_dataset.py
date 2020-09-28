from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites.site_model_mixin import SiteModelMixin
from edc_identifier.model_mixins import UniqueSubjectIdentifierFieldMixin


class MaternalDataset(
        UniqueSubjectIdentifierFieldMixin, SiteModelMixin, BaseUuidModel):

    protocol = models.CharField(max_length=150)

    infant_identifier = models.CharField(max_length=150, unique=True)

    delivery_date = models.DateField()

    site_name = models.CharField(max_length=150)

    enrollment_date = models.DateField()

    delivery_method = models.CharField(max_length=150)

    delivery_location = models.CharField(max_length=150)

    enrollment_age = models.IntegerField()

    hiv_status = models.CharField(max_length=150)

    parity = models.IntegerField()

    gravida = models.IntegerField()

    educational_level = models.CharField(max_length=150)

    marital_status = models.CharField(max_length=150)

    personal_earnings = models.DecimalField(decimal_places=2, max_digits=10)

    source_of_income = models.CharField(max_length=150)

    occupation = models.CharField(max_length=150)

    pregarv_strat = models.CharField(max_length=150)

    arvstart_date = models.DateField()

    baseline_cd4 = models.IntegerField()

    baseline_cd4date = models.DateField()

    baseline_vl = models.IntegerField()

    baseline_vldate = models.DateField()

    baseline_hgb = models.DecimalField(decimal_places=1, max_digits=10)

    baseline_hgbdt = models.DateField()

    death_date = models.DateField()

    cooking_method = models.CharField(max_length=200)

    home_eletrified = models.CharField(max_length=150)

    house_type = models.CharField(max_length=150)

    toilet = models.IntegerField()

    toilet_indoors = models.CharField(max_length=150)

    toilet_private = models.CharField(max_length=150)

    piped_water = models.CharField(max_length=150)

    home_reridgeration = models.CharField(max_length=150)

    drinking_water = models.CharField(max_length=150)

    live_inhouse_number = models.IntegerField()

    class Meta:
        app_label = 'flourish_maternal'
        verbose_name = 'Maternal Dataset'
