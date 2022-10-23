from django.apps import apps as django_apps
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
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
        validators=[MaxValueValidator(1440), ],
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
    def ra_users(self):
        """Return a list of users that can be assigned an issue.
        """
        ras_choices = ()
        user = django_apps.get_model('auth.user')
        app_config = django_apps.get_app_config('flourish_caregiver')
        ras_group = app_config.ras_group
        try:
            Group.objects.get(name=ras_group)
        except Group.DoesNotExist:
            pass

        ras = user.objects.filter(
            groups__name=ras_group)
        extra_choices = ()
        if app_config.extra_assignee_choices:
            for _, value in app_config.extra_assignee_choices.items():
                extra_choices += (value[0],)
        for ra in ras:
            username = ra.username
            if not ra.first_name:
                raise ValidationError(
                    f"The user {username} needs to set their first name.")
            if not ra.last_name:
                raise ValidationError(
                    f"The user {username} needs to set their last name.")
            full_name = (f'{ra.first_name} '
                         f'{ra.last_name}')
            ras_choices += ((username, full_name),)
        if extra_choices:
            ras_choices += extra_choices
        return ras_choices

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'TB Interview'
