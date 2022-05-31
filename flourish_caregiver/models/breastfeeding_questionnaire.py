from django.db import models
from .model_mixins import CrfModelMixin
from edc_protocol.validators import datetime_not_before_study_start
from edc_base.model_validators import datetime_not_future
from edc_base.utils import get_utcnow
from ..choices import (HIV_STATUS_AWARE,FEEDING_HIV_STATUS,
                       ON_HIV_STATUS_AWARE,HIV_STATUS,HIV_STATUS_KNOWN_BY,HIV_STATUS_KNOWN_BY_FATHER,
                       ADVICED,AGREE_DISAGREE,BREASTFEEDING_DURATION, FEEDING_ADVICE,
                       AFTER_BIRTH_OPINION,FEEDING_INFLUENCE,RETURNED_TO_WORK,FEEDING_AFTER_SIX_MONTHS)
from .list_models import (PregnancyInfluencersList,AfterPregnancyInfluencersList,ReceivedTrainingOnFeedingList,
                          ReasonsForInfantFeedingList)
from edc_base.model_fields import OtherCharField


class BreastFeedingQuestionnaire(CrfModelMixin):
    
    report_datetime = models.DateTimeField(
        verbose_name='Report Time and Date',
        default=get_utcnow,
        validators=[datetime_not_future, datetime_not_before_study_start],)
    
    
    feeding_hiv_status = models.CharField(
        verbose_name='I was aware of my HIV status when I made my infant feeding choice',
        max_length=18,
        choices=FEEDING_HIV_STATUS)
    
    hiv_status_aware = models.CharField(
        verbose_name='I was not aware of my HIV status when I first made a plan '
        'for feeding my infant, but I became aware of my HIV status:',
        max_length=18,
        choices=HIV_STATUS_AWARE)
    
    on_hiv_status_aware = models.CharField(
        verbose_name='When you became aware of your HIV status, did you change'
        ' your infant feeding choice?',
        max_length=8,
        choices=ON_HIV_STATUS_AWARE,
    )
    
    hiv_status_during_preg = models.CharField(
        verbose_name='My HIV status during pregnancy and/or breastfeeding was:',
        max_length=10,
        choices=HIV_STATUS,    
    )
    
    hiv_status_known_by = models.CharField(
        verbose_name='During my pregnancy or breastfeeding, my HIV status was known by:',
        max_length=14,
        choices=HIV_STATUS_KNOWN_BY,    
    )
    
    father_knew_hiv_status = models.CharField(
        verbose_name='During my pregnancy or breastfeeding, my HIV status was known by the father of this baby.',
        max_length=4,
        choices=HIV_STATUS_KNOWN_BY_FATHER,    
    )
    
    delivery_advice_vl_results = models.CharField(
        verbose_name='At delivery, I was advised not to breastfeed my infant because I did not have a recent viral load result.',
        max_length=16,
        choices=ADVICED,    
    )
    
    delivery_advice_on_viralload = models.CharField(
        verbose_name='At delivery, I was advised not to breastfeed my infant because my viral load was too high.',
        max_length=16,
        choices=ADVICED,    
    )
    
    after_delivery_advice_vl_results = models.CharField(
        verbose_name='n the months after delivery, I was advised not to breastfeed my infant '
        'because I did not have recent viral load results.',
        max_length=16,
        choices=ADVICED,    
    )
    
    after_delivery_advice_on_viralload = models.CharField(
        verbose_name='In the months after delivery, I was advised not '
        'to breastfeed my infant because my viral load was too high.',
        max_length=16,
        choices=ADVICED,    
    )
    
    use_medicines = models.CharField(
        verbose_name='I feIt that I could breastfeed and still keep my baby from getting'
        ' HIV by using antiretroviral medicines.',
        max_length=20,
        choices=AGREE_DISAGREE,
    )
    
    breastfeeding_duration = models.CharField(
        verbose_name='What do you think the correct duration of breastfeeding should '
        'be if a mother has HIV but is taking antiretroviral treatment to prevent '
        'mother-to-child HIV transmission throughout breastfeeding?',
        max_length=30,
        choices=BREASTFEEDING_DURATION,
    )
    
    during_preg_influencers = models.ManyToManyField(
        PregnancyInfluencersList,
        verbose_name='During pregnancy, the individuals most influential in helping me '
        'plan a feeding choice for this baby were (select 3):',
        blank=True,)
    
    during_preg_influencers_other = OtherCharField(
        verbose_name="if other specify...",
        max_length=200,
        blank=True,
        null=True)
    
    influenced_during_preg = models.CharField(
        verbose_name='During pregnancy, I felt that others influenced me to plan a '
        'feeding choice for this baby that was not my own preference.',
        max_length=20,
        choices=AGREE_DISAGREE,
    )
    
    after_delivery_influencers = models.ManyToManyField(
        AfterPregnancyInfluencersList,
        verbose_name='Since this baby was born, the individuals most influential in '
        'helping me make a feeding choice for this baby have been (select 3):',
        blank=True,)
    
    after_delivery_influencers_other = OtherCharField(
        verbose_name="if other specify...",
        max_length=200,
        blank=True,
        null=True)
    
    influenced_after_delivery = models.CharField(
        verbose_name='Since this baby was born, I felt that others influenced me to plan a '
        'feeding choice for this baby that was not my own preference.',
        max_length=20,
        choices=AGREE_DISAGREE,
    )
    
    received_training = models.ManyToManyField(
        ReceivedTrainingOnFeedingList,
        verbose_name='I have received training about the risks and benefits of breast '
        'and formula feeding from (select all that apply):',
        blank=True,
    )
    
    training_outcome = models.CharField(
        verbose_name='The training increased my understanding of the risk and benefits of breastfeeding and formula feeding.',
        max_length=20,
        choices=AGREE_DISAGREE,
    )
    
    feeding_advice = models.CharField(
        verbose_name='I was advised by a health worker to feed my baby by:',
        max_length=20,
        choices=FEEDING_ADVICE,
    )
    
    training_outcome = models.CharField(
        verbose_name='The training increased my understanding of the risk and benefits of breastfeeding and formula feeding.',
        max_length=20,
        choices=AGREE_DISAGREE,
    )
    
    community_breastfeeding_bias = models.CharField(
        verbose_name='In my community, if a woman does not breastfeed her infant and only '
        'uses infant formula/other foods, people will be suspicious she has HIV.',
        max_length=20,
        choices=AGREE_DISAGREE,
    )
    
    community_exclusive_breastfeeding_bias = models.CharField(
        verbose_name='In my community, if a woman exclusively breastfeed her infant and only '
        'uses infant formula/other foods, people will be suspicious she has HIV.',
        max_length=20,
        choices=AGREE_DISAGREE,
    )
    
    after_birth_opinion = models.CharField(
        verbose_name='In the months since this baby was born, I:',
        max_length=35,
        choices=AFTER_BIRTH_OPINION,
    )
    
    return_to_work_school = models.CharField(
        verbose_name='My need to return to work/school influenced my feeding choice for this baby.',
        max_length=3,
        choices=FEEDING_INFLUENCE,
    )
    
    returned_to_work_school = models.CharField(
        verbose_name='My need to return to work/school influenced my feeding choice for this baby.',
        max_length=40,
        choices=RETURNED_TO_WORK,
    )
    
    six_months_feeding = models.CharField(
        verbose_name='My need to return to work/school influenced my feeding choice for this baby.',
        max_length=16,
        choices=FEEDING_AFTER_SIX_MONTHS,
    )
    
    infant_feeding_reasons = models.ManyToManyField(
        ReasonsForInfantFeedingList,
        verbose_name='I introduced infant formula or other foods besides breastmilk because (select all that apply):',
        blank=True,)
    
    infant_feeding_other = OtherCharField(
        max_length=150,
        verbose_name="if other specify...",
        blank=True,
        null=True,)
    
    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Breast Feeding Questionnaire'
        verbose_name_plural = 'Breast Feeding Questionnaire'

        
    
    
    
    
    