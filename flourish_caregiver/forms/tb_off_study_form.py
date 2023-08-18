from django import forms
from django.apps import apps as django_apps
from django.forms import ValidationError
from edc_form_validators import FormValidator
from edc_form_validators import FormValidatorMixin

from flourish_caregiver.models import TbOffStudy, TbVisitScreeningWomen
from flourish_caregiver.models import TbRoutineHealthScreen, TbPresenceHouseholdMembers


class TbOffStudyForm(FormValidatorMixin, FormValidator, forms.ModelForm):

    def clean(self):
        super().clean()

        self.validate_other_specify(
            field='reason',
            other_specify_field='reason_other',
        )
        self.validate_against_latest_visit()
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

    def validate_against_latest_visit(self):
        self.visit_cls = django_apps.get_model(
            'flourish_caregiver.maternalvisit')

        subject_identifier = self.cleaned_data.get('subject_identifier')
        latest_visit = self.visit_cls.objects.filter(
            appointment__subject_identifier=subject_identifier).order_by(
            '-report_datetime').first()

        report_datetime = self.cleaned_data.get('report_datetime')
        offstudy_date = self.cleaned_data.get('offstudy_date')

        if latest_visit:
            latest_visit_datetime = latest_visit.report_datetime

            if report_datetime < latest_visit.report_datetime:
                raise forms.ValidationError({
                    'report_datetime': 'Report datetime cannot be '
                    f'before previous visit Got {report_datetime} '
                    f'but previous visit is {latest_visit_datetime}'
                })
            if offstudy_date and \
                    offstudy_date < latest_visit.report_datetime.date():
                raise forms.ValidationError({
                    'offstudy_date': 'Offstudy date cannot be '
                    f'before previous visit Got {offstudy_date} '
                    f'but previous visit is {latest_visit_datetime.date()}'
                })

    class Meta:
        model = TbOffStudy
        fields = '__all__'
