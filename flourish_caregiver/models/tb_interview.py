from django.apps import apps as django_apps
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from ..choices import INTERVIEW_LOCATIONS, INTERVIEW_LANGUAGE
from .model_mixins import CrfModelMixin


class TbInterview(CrfModelMixin):

    interview_location = models.CharField(
        verbose_name='Location of the interview',
        choices=INTERVIEW_LOCATIONS,
        max_length=100)

    interview_location_other = models.TextField(
        verbose_name='If other, specify ',
        max_length=100,
        null=True,
        blank=True)

    interview_duration = models.PositiveIntegerField(
        verbose_name='Duration of interview:',
        validators=[MinValueValidator(10), MaxValueValidator(1440)],
        help_text='Insert number of minutes')

    # # mp3 upload field
    interview_file = models.FileField(upload_to='tb_int/', null=True)

    interview_language = models.CharField(
        verbose_name='In what language was the interview performed? ',
        choices=INTERVIEW_LANGUAGE,
        max_length=10)

    translation_date = models.DateField(
        verbose_name='Date translation completed',
        null=True,
        blank=True)

    translator_name = models.CharField(
        verbose_name='Name of staff who performed translation',
        max_length=30,
        blank=True,
        null=True)

    interview_translation = models.FileField(
        upload_to='tb_int/docs/',
        null=True,
        blank=True)

    transcription_date = models.DateField(
        verbose_name='Date transcription completed',
        null=True,
        blank=True)

    transcriber_name = models.CharField(
        verbose_name='Name of staff who performed transcription',
        max_length=30,
        blank=True,
        null=True)

    interview_transcription = models.FileField(
        upload_to='tb_int/docs/',
        null=True,
        blank=True)

    @property
    def intv_users(self):
        """Return a list of users that can be assigned an issue.
        """
        intv_choices = ()
        user = django_apps.get_model('auth.user')
        app_config = django_apps.get_app_config('flourish_caregiver')
        interviewers_group = app_config.interviewers_group
        try:
            Group.objects.get(name=interviewers_group)
        except Group.DoesNotExist:
            pass

        interviewers = user.objects.filter(
            groups__name=interviewers_group)
        extra_choices = ()
        if app_config.extra_assignee_choices:
            for _, value in app_config.extra_assignee_choices.items():
                extra_choices += (value[0],)
        for intv in interviewers:
            username = intv.username
            if not intv.first_name:
                raise ValidationError(
                    f"The user {username} needs to set their first name.")
            if not intv.last_name:
                raise ValidationError(
                    f"The user {username} needs to set their last name.")
            full_name = (f'{intv.first_name} '
                         f'{intv.last_name}')
            intv_choices += ((username, full_name),)
        if extra_choices:
            intv_choices += extra_choices
        return intv_choices

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Interview'
