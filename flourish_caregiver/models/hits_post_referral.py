from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO_DWTA, YES_NO

from .list_models import ReasonsUnvisited, HITSSupportType, HITSHealthImproved
from .model_mixins import CrfModelMixin
from ..choices import NO_SUPPORT_REASONS, PERCEPTIONS


class HITSPostReferral(CrfModelMixin):

    visited_referral_site = models.CharField(
        verbose_name=('Since you were referred for support regarding '
                      'relationship challenges at the last attended '
                      'visit, did you go to the referral site?'),
        choices=YES_NO_DWTA,
        max_length=20)

    reason_unvisited = models.ManyToManyField(
        ReasonsUnvisited,
        verbose_name='What is the reason you did not go to the referral site',
        blank=True)

    reason_unvisited_other = OtherCharField()

    received_support = models.CharField(
        verbose_name=('Did you receive support when you went to the referral'
                      ' site?'),
        choices=YES_NO_DWTA,
        max_length=20,
        blank=True,
        null=True)

    no_support_reason = models.CharField(
        verbose_name=('What is the reason for not receiving support at the '
                      'referral site?'),
        choices=NO_SUPPORT_REASONS,
        max_length=40,
        blank=True,
        null=True)

    no_support_reason_other = OtherCharField()

    support_type = models.ManyToManyField(
        HITSSupportType,
        verbose_name='What kind of support did you receive?',
        blank=True)

    support_type_other = OtherCharField()

    health_improved = models.ManyToManyField(
        HITSHealthImproved,
        verbose_name='Since you received support, how has your health improved?',
        blank=True)

    health_improved_other = OtherCharField()

    supp_member_percept = models.CharField(
        verbose_name=('How did you perceive the person who provided support '
                      '(support member, social worker or psychologist)?'),
        choices=PERCEPTIONS,
        max_length=30,
        blank=True,
        null=True)

    supp_member_percept_other = OtherCharField()

    satisfied_w_clinic = models.CharField(
        verbose_name='Are you satisfied with the clinic/facility you were referred to',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    visit_helpful = models.CharField(
        verbose_name='Did you find the visit helpful',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    additional_counseling = models.CharField(
        verbose_name='Would you like us to provide a referral for additional counselling',
        choices=YES_NO,
        max_length=3,
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'HITS Positive Screening - Post Referral'
