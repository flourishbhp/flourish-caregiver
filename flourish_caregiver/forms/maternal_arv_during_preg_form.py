import datetime

from django import forms
from django.apps import apps as django_apps
from edc_constants.constants import YES, NO

from ..helper_classes.utils import get_child_subject_identifier_by_visit
from ..models import MaternalArvDuringPreg, MaternalArvTableDuringPreg
from .form_mixins import SubjectModelFormMixin, InlineSubjectModelFormMixin

from flourish_form_validations.form_validators import MaternalArvDuringPregFormValidator
from flourish_caregiver.helper_classes.utils import get_schedule_names


class MaternalArvDuringPregForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = MaternalArvDuringPregFormValidator

    antenatal_enrollment_model = 'flourish_caregiver.antenatalenrollment'
    appointment = 'edc_appointment.appointment'
    maternal_arv = 'flourish_caregiver.maternalarv'
    maternal_preg = 'flourish_caregiver.maternalarvduringpreg'

    @property
    def appointment_cls(self):
        return django_apps.get_model(self.appointment)

    @property
    def maternal_arv_cls(self):
        return django_apps.get_model(self.maternal_arv)

    @property
    def maternal_preg_cls(self):
        return django_apps.get_model(self.maternal_preg)

    @property
    def antenatal_enrollment_cls(self):
        return django_apps.get_model(self.antenatal_enrollment_model)

    def clean(self):
        cleaned_data = super().clean()
        self.maternal_visit = self.cleaned_data.get('maternal_visit', None)
        self.schedule_names = get_schedule_names(self.maternal_visit)

        if (cleaned_data.get('took_arv') == YES
                and cleaned_data.get('is_interrupt' == NO)):
            self.validate_date_arv_stopped()
        self.validate_arv_date_start_after_enrollment()
        self.check_new_arv_start_date()
        self.validate_previous_maternal_arv_preg_arv_start_dates()
        self.validate_maternal_arv_required()
        return cleaned_data

    def validate_maternal_arv_required(self):
        maternal_arv = self.data.get(
            'maternalarvtableduringpreg_set-0-arv_code')
        took_arv = self.cleaned_data.get('took_arv')
        is_interrupt = self.cleaned_data.get('is_interrupt')
        visit_code = self.cleaned_data.get(
            'maternal_visit').visit_code
        validation_error = forms.ValidationError(
            {'took_arv': 'Please complete the maternal arv table.'})
        if took_arv and took_arv == YES and visit_code == '2000D':
            if (is_interrupt and is_interrupt == YES) and not maternal_arv:
                raise validation_error
            elif (is_interrupt and is_interrupt == NO) and maternal_arv:
                raise forms.ValidationError(
                    {'is_interrupt': 'The maternal arv table is not required'})
        elif took_arv and took_arv == YES and not maternal_arv:
            raise validation_error

    def validate_date_arv_stopped(self):
        maternal_arv_count = self.data.get(
            'maternalarvtableduringpreg_set-TOTAL_FORMS')
        arvs_with_stop_date = 0
        for i in range(int(maternal_arv_count)):
            maternal_arv = self.data.get(
                'maternalarvtableduringpreg_set-' + str(i) + '-stop_date')
            if maternal_arv:
                arvs_with_stop_date = arvs_with_stop_date + 1
        if (int(maternal_arv_count) - arvs_with_stop_date) < 3:
            raise forms.ValidationError(
                'Patient should have atleast 3 arv\'s with no stop date')

    def validate_arv_date_start_after_enrollment(self):
        child_subject_identifier = get_child_subject_identifier_by_visit(self.maternal_visit)
        try:
            antenatal_enrollment = self.antenatal_enrollment_cls.objects.get(
                subject_identifier=getattr(self.maternal_visit, 'subject_identifier', None),
                child_subject_identifier=child_subject_identifier)
        except self.antenatal_enrollment_cls.DoesNotExist:
            raise forms.ValidationError(
                'Date of HIV test required, complete Antenatal Enrollment'
                ' form before proceeding.')
        else:
            maternal_arv_count = self.data.get(
                'maternalarvtableduringpreg_set-TOTAL_FORMS')

            for i in range(int(maternal_arv_count)):
                if self.data.get('maternalarvtableduringpreg_set-' + str(i) + '-start_date'):
                    set_start_date = self.data.get(
                        'maternalarvtableduringpreg_set-' + str(i) + '-start_date')
                    date_time_obj = datetime.datetime.strptime(set_start_date,
                                                               '%Y-%m-%d')
                    if date_time_obj.date() < \
                            antenatal_enrollment.week32_test_date:
                        raise forms.ValidationError(
                            'start date of arv\'s '
                            'cannot be before date of HIV test.')

    def get_previous_visit(self, visit_obj, timepoints, subject_identifier):
        position = timepoints.index(
            visit_obj.appointment.visit_code)
        timepoints_slice = timepoints[:position]
        visit_model = django_apps.get_model(visit_obj._meta.label_lower)

        if len(timepoints_slice) > 1:
            timepoints_slice.reverse()

        for point in timepoints_slice:
            previous_appointments = self.appointment_cls.objects.filter(
                subject_identifier=subject_identifier,
                visit_code=point).order_by('-created')
            prev_arv_preg = self.get_previous_arv_preg(
                appointments=previous_appointments, visit_model=visit_model)
            if prev_arv_preg:
                return point
        return None

    def check_new_arv_start_date(self):

        arv_count = self.data.get('maternalarvtableduringpreg_set-TOTAL_FORMS')

        for num in range(int(arv_count)):
            arv_stop_date = self.data.get(
                'maternalarvtableduringpreg_set-' + str(num) + '-stop_date')

            if arv_stop_date:
                arv_code = self.data.get(
                    'maternalarvtableduringpreg_set-' + str(num) + '-arv_code')
                self.validate_new_maternal_arv_preg_start_date(
                    arv_stop_date, arv_code, arv_count)

    def validate_new_maternal_arv_preg_start_date(self, stop_date, arv_code, count):
        switch_arv_code = "".join(self.arv_code_check(arv_code))

        if switch_arv_code:
            for num in range(int(count)):
                if switch_arv_code == self.data.get(
                        'maternalarvtableduringpreg_set-' + str(num) + '-arv_code'):

                    start_date = self.data.get(
                        'maternalarvtableduringpreg_set-' + str(num) + '-start_date')
                    start_date = datetime.datetime.strptime(
                        start_date, '%Y-%m-%d').date() if start_date else None

                    stop_date = datetime.datetime.strptime(
                        stop_date, '%Y-%m-%d').date() if stop_date else None

                    if start_date != stop_date:
                        raise forms.ValidationError(
                            f'Stop date {stop_date} for {arv_code}, does not match '
                            f'{switch_arv_code} {start_date} start date.')

    def arv_code_check(self, arv_code):
        ftc_3tc = ['Emtricitabine', 'Lamivudine']
        efv_dtg = ['Dolutegravir', 'Efavirenz']
        if arv_code in ftc_3tc:
            ftc_3tc.remove(arv_code)
            return ftc_3tc
        elif arv_code in efv_dtg:
            efv_dtg.remove(arv_code)
            return efv_dtg
        return []

    def get_previous_arv_preg(self, subject_identifier, report_datetime):
        prev_arv_preg = self.maternal_preg_cls.objects.filter(
            maternal_visit__subject_identifier=subject_identifier,
            maternal_visit__schedule_name__in=self.schedule_names,
            report_datetime__lt=report_datetime).order_by('-created').first()
        if prev_arv_preg:
            return prev_arv_preg
        return None

    def validate_previous_maternal_arv_preg_arv_start_dates(self):
        """Confirms that the ARV start date is equal to Maternal ARV
        start date unless stopped.
        """
        cleaned_data = self.cleaned_data
        subject_identifier = cleaned_data.get(
            'maternal_visit').appointment.subject_identifier
        report_datetime = cleaned_data.get('report_datetime')

        previous_arv_preg = self.get_previous_arv_preg(subject_identifier,
                                                       report_datetime)
        if previous_arv_preg:
            arv_count = self.data.get(
                'maternalarvtableduringpreg_set-TOTAL_FORMS')

            for index in range(int(arv_count)):
                arv_start_date = self.data.get(
                    'maternalarvtableduringpreg_set-' + str(index) + '-start_date')
                start_date = datetime.datetime.strptime(
                    arv_start_date, '%Y-%m-%d') if arv_start_date else None

                arv_code = self.data.get(
                    'maternalarvtableduringpreg_set-' + str(index) + '-arv_code')

                prev_arv = previous_arv_preg.maternalarv_set.filter(
                    arv_code=arv_code).order_by('-created').first()

                if prev_arv:
                    if start_date and start_date.date() != prev_arv.start_date:
                        raise forms.ValidationError(
                            f'Start date for {arv_code} does not match previous start date '
                            f'{prev_arv.start_date} for visit {previous_arv_preg.maternal_visit.visit_code}')

    def get_current_stopped_arv_date(self):
        """
        function that checks the most recent arv stop date and returns it
        """
        arv_count = int(self.data.get(
            'maternalarvtableduringpreg_set-TOTAL_FORMS'))
        arv_stop_dates = []

        for index in range(arv_count):
            arv_stop_date = self.data.get(
                'maternalarvtableduringpreg_set-' + str(index) + '-stop_date')
            arv_stop_dates.append(arv_stop_date)

        if arv_stop_dates and max(arv_stop_dates):
            stop_date = datetime.datetime.strptime(
                max(arv_stop_dates), '%Y-%m-%d').date()
            if stop_date:
                return stop_date

        return None

    def get_previous_stopped_arv_date(self, subject_identifier, arv_code):
        previous_arv_preg = self.maternal_arv_cls.objects.filter(
            maternal_arv_durg_preg__maternal_visit__appointment__subject_identifier=subject_identifier,
            maternal_arv_durg_preg__maternal_visit__schedule_name__in=self.schedule_names,
            arv_code=arv_code,
            stop_date__isnull=False)

        if previous_arv_preg:
            return previous_arv_preg.stop_date

    class Meta:
        model = MaternalArvDuringPreg
        fields = '__all__'


class MaternalArvTableDuringPregForm(InlineSubjectModelFormMixin):
    class Meta:
        model = MaternalArvTableDuringPreg
        fields = '__all__'
