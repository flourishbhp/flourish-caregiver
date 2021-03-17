from ..models import CaregiverChildConsent
from .form_mixins import SubjectModelFormMixin


class CaregiverChildConsentForm(SubjectModelFormMixin):

    class Meta:
        model = CaregiverChildConsent
        fields = '__all__'
