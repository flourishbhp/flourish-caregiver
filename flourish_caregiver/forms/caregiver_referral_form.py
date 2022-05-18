from django import forms
from ..models import CaregiverReferral
from .form_mixins import SubjectModelFormMixin

class CaregiverReferralForm(SubjectModelFormMixin):
    
    # add form validator
    
    class Meta:
        model = CaregiverReferral
        fields = '__all__'
