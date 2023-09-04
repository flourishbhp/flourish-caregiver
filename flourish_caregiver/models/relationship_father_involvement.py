from django.db import models
from .model_mixins import RelationshipFatherInvolvementMixin
from .model_mixins import CrfModelMixin
from flourish_caregiver.models.list_models import HouseholdMember


class RelationshipFatherInvolvement(RelationshipFatherInvolvementMixin, CrfModelMixin):
    """A CRF to be completed by biological mothers living with HIV,
    at enrollment, annual (every 4th quarterly call), and follow-up
    """
    read_books = models.ManyToManyField(
        HouseholdMember,
        related_name='caregiver_read_books',
        verbose_name='Read books or looked at picture books with your child', )

    told_stories = models.ManyToManyField(
        HouseholdMember,
        related_name='caregiver_told_stories',
        verbose_name='Told stories to your child', )

    sang_songs = models.ManyToManyField(
        HouseholdMember,
        related_name='caregiver_sang_songs',
        verbose_name='Sang songs to or with your child, including lullabies', )

    took_child_outside = models.ManyToManyField(
        HouseholdMember,
        related_name='caregiver_took_child_outside',
        verbose_name='Took your child outside the home', )

    played_with_child = models.ManyToManyField(
        HouseholdMember,
        related_name='caregiver_played_with_child',
        verbose_name='Played with your child', )

    named_with_child = models.ManyToManyField(
        HouseholdMember,
        related_name='caregiver_named_with_child',
        verbose_name='Named, counted, or drew things with or for your child', )

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Relationship and Father Involvement'
        verbose_name_plural = 'Relationship and Father Involvement'
