from django.db import models
from django.db.models import PROTECT
from edc_base.model_mixins import BaseUuidModel
from edc_visit_tracking.model_mixins import CrfInlineModelMixin

from .model_mixins import CrfModelMixin
from ..choices import RELATIONSHIP_SCALE


class ParentAdolReloScaleParentModel(CrfModelMixin):
    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Parent-Adolescent Relationship Scales'


class ParentAdolRelationshipScale(CrfInlineModelMixin, BaseUuidModel):
    parent_adol_relo_scale_parent_model = models.ForeignKey(
        ParentAdolReloScaleParentModel, on_delete=PROTECT, null=True)

    associated_child_identifier = models.CharField(
        max_length=25)

    eat_together = models.CharField(
        verbose_name="We eat meals together",
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    time_together = models.CharField(
        verbose_name="We spend time together doing activities we each like",
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    family_events_together = models.CharField(
        verbose_name="We go to family events together",
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    support_from_others = models.CharField(
        verbose_name='I encourage my child/adolescent to get support from me or others',
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    show_affection = models.CharField(
        verbose_name=('I show affection to my child/adolescent (e.g., hugs,kisses, '
                      'smiling, arm around shoulder'),
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    comfort = models.CharField(
        verbose_name='I comfort my child/adolescent when he/she is upset',
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    negative_comments = models.CharField(
        verbose_name='I make negative comments about my child/adolescent to others',
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    compassion = models.CharField(
        verbose_name='During stressful times in my child/adolescents life, I check if '
                     'he/she is okay',
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    upset = models.CharField(
        verbose_name='I get upset when my child/adolescent disagrees with me',
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    play_sport = models.CharField(
        verbose_name='I play sport or do other physical activities with my '
                     'child/adolescent',
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    complains_about_me = models.CharField(
        verbose_name='My child/adolescent complains about me',
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    encourage = models.CharField(
        verbose_name='I encourage my child/adolescent to do things he/she is interested '
                     'in or enjoys',
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    criticize_child = models.CharField(
        verbose_name='I criticize my child/adolescent',
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    change_attitude = models.CharField(
        verbose_name='I think my child/adolescent needs to change his/her attitude',
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    encourage_expression = models.CharField(
        verbose_name='I encourage my child/adolescent to talk about their thoughts and '
                     'feelings',
        max_length=2,
        choices=RELATIONSHIP_SCALE)

    @property
    def shared_activities(self):
        """ Shared Activities (4 items) (1 + 2 + 3 + 10)/4
        """
        question_1 = int(self.eat_together)
        question_2 = int(self.time_together)
        question_3 = int(self.family_events_together)
        question_10 = int(self.play_sport)

        result = (question_1 + question_2 + question_3 + question_10) / 4

        return round(result, 4)

    @property
    def connectedness(self):
        """ Connectedness (6 items) (4 + 5 + 6 + 8 + 12 + 15)/6
        """
        question_4 = int(self.support_from_others)
        question_5 = int(self.show_affection)
        question_6 = int(self.comfort)
        question_8 = int(self.compassion)
        question_12 = int(self.encourage)
        question_15 = int(self.encourage_expression)

        result = (question_4 + question_5 + question_6 +
                  question_8 + question_12 + question_15) / 6

        return round(result, 4)

    @property
    def hostility(self):
        """ Hostility (5 items) (7 + 9 + 11 + 13 + 14)/5
        """

        question_7 = int(self.negative_comments)
        question_9 = int(self.upset)
        question_11 = int(self.complains_about_me)
        question_13 = int(self.criticize_child)
        question_14 = int(self.change_attitude)
        result = (question_7 + question_9 + question_11 + question_13 + question_14) / 5

        return round(result, 4)

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Parent-Adolescent Relationship Scale'
