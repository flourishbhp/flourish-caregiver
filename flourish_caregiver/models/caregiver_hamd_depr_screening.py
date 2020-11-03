from django.db import models

from .model_mixins import CrfModelMixin
from ..choices import (DEPRESSION_MOOD, GUILT_FEELINGS, SUICIDAL, INSOMNIA_INITIAL,
                       INSOMIA_MIDNIGHT, INSOMNIA_EARLY, WORK_INTERESTS, AGITATION,
                       RETARDATION, ANXIETY, ANXIETY_PYSCHIC, SOMATIC_SYMPTOMS,
                       HYPOCHONDRIASIS, WEIGHT_LOSS, INSIGHT, GENERAL_SOMATIC,
                       GENITAL_SYMPTOMS)


class CaregiverHamdDeprScreening(CrfModelMixin):

    depressed_mood = models.CharField(
        verbose_name=('Depressed Mood (Gloomy attitude, pessimism about the '
                      'future, feeling of sadness, tendency to weep)'),
        choices=DEPRESSION_MOOD,
        max_length=2)

    guilt_feelings = models.CharField(
        verbose_name=('Feelings Of Guilt'),
        choices=GUILT_FEELINGS,
        max_length=2)

    suicidal = models.CharField(
        verbose_name=('Suicide'),
        choices=SUICIDAL,
        max_length=2)

    insomnia_initial = models.CharField(
        verbose_name=('Insomnia – Initial (Difficulty in falling asleep)'),
        choices=INSOMNIA_INITIAL,
        max_length=2)

    insomnia_middle = models.CharField(
        verbose_name=('Insomnia – Middle (Complains of being restless and '
                      'disturbed during the night. Waking during the night.)'),
        choices=INSOMIA_MIDNIGHT,
        max_length=2)

    insomnia_delayed = models.CharField(
        verbose_name=('Insomnia – Delayed (Waking in early hours of the '
                      'morning and unable to fall asleep again)'),
        choices=INSOMNIA_EARLY,
        max_length=2)

    work_interests = models.CharField(
        verbose_name=('Work and Interests'),
        choices=WORK_INTERESTS,
        max_length=2)

    retardation = models.CharField(
        verbose_name=('Retardation (Slowness of thought, speech, and activity;'
                      ' apathy; stupor.)'),
        choices=RETARDATION,
        max_length=2)

    agitation = models.CharField(
        verbose_name=('Agitation (Restlessness associated with anxiety.)'),
        choices=AGITATION,
        max_length=2)

    anxiety_pyschic = models.CharField(
        verbose_name=('Anxiety – Psychic'),
        choices=ANXIETY_PYSCHIC,
        max_length=2)

    anxiety = models.CharField(
        verbose_name=('Anxiety – Somatic Gastrointestinal, indigestion, '
                      'Cardiovascular, palpitation, Headaches, Respiratory, '
                      'Genito-urinary, etc'),
        choices=ANXIETY,
        max_length=2)

    gastro_symptoms = models.CharField(
        verbose_name=('Somatic Symptoms – Gastrointestinal (Loss of appetite ,'
                      ' heavy feeling in abdomen; constipation)'),
        choices=SOMATIC_SYMPTOMS,
        max_length=2)

    general_symptoms = models.CharField(
        verbose_name=('Somatic Symptoms – General (Heaviness in limbs, back or'
                      ' head; diffuse backache; loss of energy and fatiguability)'),
        choices=GENERAL_SOMATIC,
        max_length=2)

    genital_symptoms = models.CharField(
        verbose_name=('Genital Symptoms (Loss of libido, menstrual disturbances)'),
        choices=GENITAL_SYMPTOMS,
        max_length=2)

    hypochondriasis = models.CharField(
        verbose_name=('Hypochondriasis'),
        choices=HYPOCHONDRIASIS,
        max_length=2)

    weight_loss = models.CharField(
        verbose_name=('Weight Loss'),
        choices=WEIGHT_LOSS,
        max_length=2)

    insight = models.CharField(
        verbose_name=('Insight'),
        choices=INSIGHT,
        max_length=2,
        help_text='(Insight must be interpreted in terms of patient’s understanding and background.)')

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Depression Screening - HAM-D'
        verbose_name_plural = 'Depression Screening - HAM-D'
