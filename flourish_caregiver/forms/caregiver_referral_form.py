from ..models import CaregiverReferral
from .form_mixins import SubjectModelFormMixin


class CaregiverReferralForm(SubjectModelFormMixin):

    class Meta:
        model = CaregiverReferral
        fields = '__all__'
