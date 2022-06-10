from django import forms
from edc_form_validators import FormValidatorMixin

from flourish_caregiver.models import TbOffStudy, TbVisitScreeningWomen, \
    TbRoutineHealthScreen, TbPresenceHouseholdMembers
from flourish_prn.form_validations import OffstudyFormValidator
from django.forms import ValidationError


class TbOffStudyForm(FormValidatorMixin, forms.ModelForm):
    form_validator_cls = OffstudyFormValidator

    def clean(self):
        super(TbOffStudyForm, self).clean()
        self.validate_required_forms()

    def validate_required_forms(self):
        subject_identifier = self.cleaned_data.get('subject_identifier')
        tb_visit_screening_objs = TbVisitScreeningWomen.objects.filter(
            maternal_visit__subject_identifier=subject_identifier).count()
        tb_routine_screening_objs = TbRoutineHealthScreen.objects.filter(
            maternal_visit__subject_identifier=subject_identifier).count()
        tb_in_house_members_objs = TbPresenceHouseholdMembers.objects.filter(
            maternal_visit__subject_identifier=subject_identifier).count()

        if (tb_visit_screening_objs < 0 and
                tb_routine_screening_objs < 0 and
                tb_in_house_members_objs < 0):
            ValidationError(f'Please make sure that the following forms\n'
                            f'- Tb screen at 2 months Postpartum\n'
                            f'- Screen for TB at routine health encounters\n'
                            f'- TB symptoms in household members at 2 months postpartum')


    class Meta:
        model = TbOffStudy
        fields = '__all__'
