import mimetypes
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy
from edc_base.model_mixins import BaseUuidModel
from edc_base.utils import get_utcnow
from edc_consent.field_mixins import VerificationFieldsMixin

from .model_mixins import CrfModelMixin


# Define a custom validator
def validate_image_or_pdf(file):
    # Check file type (you can extend this logic for more file types)
    valid_image_types = ['image/jpeg', 'image/png', 'image/gif']
    valid_pdf_type = 'application/pdf'
    file_type, _ = mimetypes.guess_type(file.name)

    if (file_type not in valid_image_types and
            file_type != valid_pdf_type):
        raise ValidationError(
            gettext_lazy('Only image files and PDF files are allowed.'))


class ClinicianNotes(VerificationFieldsMixin, CrfModelMixin):
    crf_date_validator_cls = None

    class Meta(CrfModelMixin.Meta):
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Clinician Notes'
        verbose_name_plural = 'Caregiver Clinician Notes'


class ClinicianNotesImage(BaseUuidModel):
    clinician_notes = models.ForeignKey(
        ClinicianNotes,
        on_delete=models.PROTECT,
        related_name='caregiver_clinician_notes', )

    image = models.FileField(
        upload_to='caregiver_notes/',
        validators=[validate_image_or_pdf])

    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded', )

    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def clinician_notes_image(self):
        # Get the file type
        file_url = getattr(self.image, 'url', None)
        file_type, _ = mimetypes.guess_type(file_url)

        # Check if it's an image
        if file_type:
            if file_type.startswith('image'):
                return mark_safe(
                    f'<a href="{file_url}" target="_blank">'
                    f'<img src="{file_url}" style="padding-right:150px" width="150" height="100" />'
                    '</a>'
                )
            # If it's a PDF (or other file type)
            elif file_type == 'application/pdf':
                return mark_safe(
                    f'<a href="{file_url}" target="_blank">View PDF</a>'
                )
            else:
                return mark_safe('-')

    clinician_notes_image.short_description = 'Clinician Notes Image'
    clinician_notes_image.allow_tags = True

    class Meta:
        app_label = 'flourish_caregiver'
        verbose_name = 'Caregiver Clinician Notes Image'
        verbose_name_plural = 'Caregiver Clinician Notes Images'
